"""產生示意圖：預測 vs 專家散點圖、Bland–Altman 圖、Grad-CAM 疊圖。

用合成資料訓練 MVP 後輸出三張圖到 docs/assets/，作為「管線可視化」的佐證。
⚠️ 圖中數據來自合成資料，僅示範流程，不具臨床意義。
執行：python scripts/make_figures.py
"""
from __future__ import annotations

import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from raxray.config import Config, set_seed
from raxray.data.synthetic import generate_dataset
from raxray.data.dataset import split_by_patient, HandXrayDataset
from raxray.train import train, predict
from raxray.evaluate import regression_report, bland_altman
from raxray.gradcam import GradCAM
from raxray.models.ordinal import corn_expected_rank

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "assets")
os.makedirs(OUT, exist_ok=True)


def main():
    cfg = Config(image_size=128, num_classes=4, backbone="resnet18", pretrained=True,
                 head_type="ordinal", batch_size=16, lr=1e-3, epochs=15,
                 early_stop_patience=6, num_workers=0, seed=42)
    set_seed(cfg.seed)
    samples = generate_dataset(60, 2, cfg.image_size, cfg.num_classes, cfg.score_max, cfg.seed)
    tr, va, te = split_by_patient(samples, cfg.val_frac, cfg.test_frac, cfg.seed)
    train_ds = HandXrayDataset(tr, cfg.image_size, train=True, seed=cfg.seed)
    val_ds = HandXrayDataset(va, cfg.image_size, train=False, seed=cfg.seed)
    test_ds = HandXrayDataset(te, cfg.image_size, train=False, seed=cfg.seed)

    model, _ = train(train_ds, val_ds, cfg, log=lambda *a: None)
    sp, gp, st, gt = predict(model, test_ds, cfg)
    rep = regression_report(st, sp, n_boot=500, seed=cfg.seed)

    # 圖 1：預測 vs 專家 散點
    plt.figure(figsize=(5, 5))
    lim = max(st.max(), sp.max()) * 1.05
    plt.plot([0, lim], [0, lim], "k--", lw=1, label="Ideal (y=x)")
    plt.scatter(st, sp, c="#2a6", alpha=0.7, edgecolors="k", linewidths=0.3)
    plt.xlabel("Expert score (synthetic)")
    plt.ylabel("Model predicted score")
    plt.title(f"Predicted vs Expert  (ICC={rep['icc_2_1']:.2f}, r={rep['pearson_r']:.2f})")
    plt.legend(); plt.tight_layout()
    plt.savefig(os.path.join(OUT, "fig1_scatter.png"), dpi=120); plt.close()

    # 圖 2：Bland–Altman
    ba = bland_altman(st, sp)
    mean_ax = (st + sp) / 2
    diff = sp - st
    plt.figure(figsize=(5.5, 4.2))
    plt.scatter(mean_ax, diff, c="#36c", alpha=0.7, edgecolors="k", linewidths=0.3)
    plt.axhline(ba.bias, color="k", lw=1.2, label=f"bias={ba.bias:.1f}")
    plt.axhline(ba.loa_upper, color="r", ls="--", lw=1, label=f"+1.96SD={ba.loa_upper:.1f}")
    plt.axhline(ba.loa_lower, color="r", ls="--", lw=1, label=f"-1.96SD={ba.loa_lower:.1f}")
    plt.xlabel("Mean of expert & model"); plt.ylabel("Model - Expert")
    plt.title("Bland-Altman agreement (synthetic)")
    plt.legend(fontsize=8); plt.tight_layout()
    plt.savefig(os.path.join(OUT, "fig2_bland_altman.png"), dpi=120); plt.close()

    # 圖 3：Grad-CAM 疊圖
    cam_engine = GradCAM(model, model.feature_layer)
    # 取一張嚴重度較高的樣本，視覺較明顯
    idx = int(np.argmax([test_ds.samples[i].grade for i in range(len(test_ds))]))
    sample = test_ds[idx]
    cam = cam_engine(sample["image"].unsqueeze(0),
                     scalar_fn=lambda l: corn_expected_rank(l).sum())
    base = sample["image"][0].numpy()
    base = (base - base.min()) / (base.max() - base.min() + 1e-6)
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1); plt.imshow(base, cmap="gray"); plt.title("Synthetic hand X-ray"); plt.axis("off")
    plt.subplot(1, 2, 2); plt.imshow(base, cmap="gray"); plt.imshow(cam, cmap="jet", alpha=0.45)
    for x0, y0, x1, y1 in sample["joint_boxes"].numpy():
        plt.gca().add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0,
                            fill=False, edgecolor="lime", lw=1))
    plt.title("Grad-CAM (joints in green)"); plt.axis("off")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "fig3_gradcam.png"), dpi=120); plt.close()

    print("已輸出 3 張圖到 docs/assets/")
    print(f"ICC={rep['icc_2_1']:.3f} Pearson={rep['pearson_r']:.3f} RMSE={rep['rmse']:.1f}")


if __name__ == "__main__":
    main()
