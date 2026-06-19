"""端到端 smoke test：用合成資料把整條 MVP 管線跑通並驗證正確性。

涵蓋：合成資料 → 病人層級切分（防外洩 assert）→ 前處理 → 訓練（CORN 序數）
→ 推論 → 評估（ICC/Bland–Altman/相關/RMSE + 分級 QWK）→ Grad-CAM 量化。

這支腳本不需要任何真實資料，可在 CPU 上於數分鐘內跑完，用來證明
「資料一到位就能直接上線」。執行：python scripts/smoke_test.py
"""
from __future__ import annotations

import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from raxray.config import Config, set_seed
from raxray.data.synthetic import generate_dataset
from raxray.data.dataset import split_by_patient, HandXrayDataset
from raxray.train import train, predict
from raxray.evaluate import regression_report, classification_report
from raxray.gradcam import GradCAM, energy_in_boxes
from raxray.models.ordinal import corn_expected_rank


def main():
    # 小規模設定，讓 CPU 也能快速跑完（真實使用請改用 docs/03 的設定）
    cfg = Config(
        image_size=128, num_classes=4, backbone="resnet18",
        pretrained=True,             # 遷移學習：用 ImageNet 預訓練權重（首次會自動下載）
        head_type="ordinal", batch_size=16, lr=1e-3, epochs=15,
        early_stop_patience=6, num_workers=0, seed=42,
    )
    set_seed(cfg.seed)
    print(f"[env] device={cfg.resolved_device()} torch={torch.__version__}")

    # 1) 合成資料
    samples = generate_dataset(n_patients=60, imgs_per_patient=2,
                               image_size=cfg.image_size, num_classes=cfg.num_classes,
                               score_max=cfg.score_max, seed=cfg.seed)
    print(f"[data] 共 {len(samples)} 張影像 / {len({s.patient_id for s in samples})} 位病人")

    # 2) 病人層級切分（內含防外洩 assert）
    tr, va, te = split_by_patient(samples, cfg.val_frac, cfg.test_frac, seed=cfg.seed)
    tr_pid = {s.patient_id for s in tr}
    te_pid = {s.patient_id for s in te}
    assert tr_pid.isdisjoint(te_pid), "資料外洩！train/test 病人重疊"
    print(f"[split] train={len(tr)} val={len(va)} test={len(te)}（病人無跨集 ✓）")

    train_ds = HandXrayDataset(tr, cfg.image_size, train=True, seed=cfg.seed)
    val_ds = HandXrayDataset(va, cfg.image_size, train=False, seed=cfg.seed)
    test_ds = HandXrayDataset(te, cfg.image_size, train=False, seed=cfg.seed)

    # 3) 訓練
    print("[train] 開始訓練 MVP（CORN 序數分級）...")
    model, best_val = train(train_ds, val_ds, cfg)
    print(f"[train] 最佳驗證損失={best_val:.4f}")

    # 4) 推論 + 評估（測試集只用這一次）
    sp, gp, st, gt = predict(model, test_ds, cfg)
    reg = regression_report(st, sp, n_boot=500, seed=cfg.seed)
    clf = classification_report(gt, gp, cfg.num_classes)

    print("\n===== 測試集評估（合成資料）=====")
    print(f"  ICC(2,1)      = {reg['icc_2_1']:.3f}  95%CI={tuple(round(v,3) for v in reg['icc_2_1_ci95'])}")
    print(f"  Pearson r     = {reg['pearson_r']:.3f}  (p={reg['pearson_p']:.2e})")
    print(f"  Spearman r    = {reg['spearman_r']:.3f}")
    print(f"  RMSE          = {reg['rmse']:.2f}  95%CI={tuple(round(v,2) for v in reg['rmse_ci95'])}")
    print(f"  MAE           = {reg['mae']:.2f}")
    ba = reg["bland_altman"]
    print(f"  Bland-Altman  : bias={ba['bias']:.2f}, LoA=[{ba['loa_lower']:.2f}, {ba['loa_upper']:.2f}]")
    print(f"  Accuracy      = {clf['accuracy']:.3f}")
    print(f"  QWK           = {clf['quadratic_weighted_kappa']:.3f}")
    print(f"  Confusion     = {clf['confusion_matrix']}")

    # 5) Grad-CAM 量化：熱區能量落在關節框內的比例 vs 隨機基準
    #    對多張測試影像平均，比單張更穩健（對應 docs/04 的量化可解釋性）。
    cam_engine = GradCAM(model, model.feature_layer)
    rng = np.random.default_rng(0)
    real_ratios, rand_ratios = [], []
    n_eval = min(10, len(test_ds))
    for i in range(n_eval):
        sample = test_ds[i]
        cam = cam_engine(sample["image"].unsqueeze(0),
                         scalar_fn=lambda logits: corn_expected_rank(logits).sum())
        boxes = sample["joint_boxes"].numpy()
        real_ratios.append(energy_in_boxes(cam, boxes))
        H, W = cam.shape
        bw = (boxes[:, 2] - boxes[:, 0]).mean()
        bh = (boxes[:, 3] - boxes[:, 1]).mean()
        rb = []
        for _ in range(len(boxes)):
            x0r = rng.integers(0, max(1, int(W - bw)))
            y0r = rng.integers(0, max(1, int(H - bh)))
            rb.append([x0r, y0r, x0r + bw, y0r + bh])
        rand_ratios.append(energy_in_boxes(cam, np.array(rb)))
    real_mean, rand_mean = float(np.mean(real_ratios)), float(np.mean(rand_ratios))
    print(f"\n  Grad-CAM 關節區能量比例 = {real_mean:.3f}  "
          f"(隨機框基準 ≈ {rand_mean:.3f}；n={n_eval} 張平均)")

    # 6) 健全性斷言：管線必須真的「學到東西」（在合成資料上應顯著優於亂猜）
    assert not np.isnan(reg["icc_2_1"]), "ICC 計算失敗"
    assert reg["pearson_r"] > 0.2, f"相關過低，管線可能有問題：r={reg['pearson_r']:.3f}"
    print("\n[OK] 端到端管線驗證通過 ✓（合成資料上模型確實學到訊號）")


if __name__ == "__main__":
    main()
