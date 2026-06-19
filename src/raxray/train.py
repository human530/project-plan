"""訓練迴圈（對應 docs/03：early stopping、checkpoint、AMP、可重現）。

支援 ordinal(CORN) 與 regression 兩種頭。回傳訓練好的模型與最佳驗證分數，
並把最佳權重存到 out_dir/ckpt_name（Colab 上請把 out_dir 指到 Google Drive）。
"""
from __future__ import annotations

import os
import time

import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader

from .config import Config
from .models.backbone import RAModel
from .models.ordinal import corn_loss, corn_expected_rank, corn_predict_label


def _make_loader(ds, cfg: Config, shuffle: bool):
    return DataLoader(ds, batch_size=cfg.batch_size, shuffle=shuffle,
                      num_workers=cfg.num_workers, drop_last=False)


def _decoded_score(logits, cfg: Config):
    """把模型輸出轉成連續 SvH 分數估計（供一致性評估用）。"""
    if cfg.head_type == "ordinal":
        rank = corn_expected_rank(logits)                 # [0, K-1]
        return rank / max(1, cfg.num_classes - 1) * cfg.score_max
    return logits.squeeze(-1) * cfg.score_max             # regression：預測標準化分數


def evaluate_loss(model, loader, cfg, device):
    model.eval()
    losses = []
    with torch.no_grad():
        for batch in loader:
            x = batch["image"].to(device)
            logits = model(x)
            if cfg.head_type == "ordinal":
                loss = corn_loss(logits, batch["grade"].to(device), cfg.num_classes)
            else:
                target = (batch["score"].to(device) / cfg.score_max)
                loss = F.smooth_l1_loss(logits.squeeze(-1), target)
            losses.append(float(loss.item()))
    return float(np.mean(losses)) if losses else float("inf")


def train(train_ds, val_ds, cfg: Config, log=print):
    device = torch.device(cfg.resolved_device())
    model = RAModel(cfg.backbone, cfg.pretrained, cfg.head_type, cfg.num_classes).to(device)

    # docs/03：先凍結骨幹做暖身，再解凍漸進式微調（小樣本防過擬合）
    model.freeze_backbone(True)
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],
                            lr=cfg.lr, weight_decay=cfg.weight_decay)
    scaler = torch.cuda.amp.GradScaler(enabled=cfg.amp and device.type == "cuda")

    train_loader = _make_loader(train_ds, cfg, shuffle=True)
    val_loader = _make_loader(val_ds, cfg, shuffle=False)

    os.makedirs(cfg.out_dir, exist_ok=True)
    ckpt_path = os.path.join(cfg.out_dir, cfg.ckpt_name)
    best_val = float("inf")
    patience = 0

    for epoch in range(cfg.epochs):
        if epoch == max(1, cfg.epochs // 5):       # 暖身後解凍骨幹微調
            model.freeze_backbone(False)
            opt = torch.optim.AdamW(model.parameters(), lr=cfg.lr * 0.3,
                                    weight_decay=cfg.weight_decay)
            log(f"[epoch {epoch}] 解凍骨幹，進入微調")

        model.train()
        t0 = time.time()
        epoch_losses = []
        for batch in train_loader:
            x = batch["image"].to(device)
            opt.zero_grad()
            with torch.autocast(device_type=device.type, enabled=cfg.amp and device.type == "cuda"):
                logits = model(x)
                if cfg.head_type == "ordinal":
                    loss = corn_loss(logits, batch["grade"].to(device), cfg.num_classes)
                else:
                    target = batch["score"].to(device) / cfg.score_max
                    loss = F.smooth_l1_loss(logits.squeeze(-1), target)
            scaler.scale(loss).backward()
            scaler.step(opt)
            scaler.update()
            epoch_losses.append(float(loss.item()))

        val_loss = evaluate_loss(model, val_loader, cfg, device)
        log(f"[epoch {epoch}] train_loss={np.mean(epoch_losses):.4f} "
            f"val_loss={val_loss:.4f} ({time.time()-t0:.1f}s)")

        if val_loss < best_val - 1e-5:
            best_val = val_loss
            patience = 0
            torch.save({"model": model.state_dict(), "cfg": cfg.to_dict()}, ckpt_path)
        else:
            patience += 1
            if patience >= cfg.early_stop_patience:
                log(f"[early stop] 連續 {patience} 個 epoch 無改善，於 epoch {epoch} 停止")
                break

    # 載回最佳權重
    if os.path.exists(ckpt_path):
        state = torch.load(ckpt_path, map_location=device)
        model.load_state_dict(state["model"])
    return model, best_val


@torch.no_grad()
def predict(model, ds, cfg: Config):
    """對資料集做推論，回傳 (scores_pred, grades_pred, scores_true, grades_true)。"""
    device = torch.device(cfg.resolved_device())
    model.eval()
    loader = _make_loader(ds, cfg, shuffle=False)
    sp, gp, st, gt = [], [], [], []
    for batch in loader:
        x = batch["image"].to(device)
        logits = model(x)
        sp.append(_decoded_score(logits, cfg).cpu().numpy())
        if cfg.head_type == "ordinal":
            gp.append(corn_predict_label(logits).cpu().numpy())
        else:
            grade = np.clip((logits.squeeze(-1).cpu().numpy() * cfg.num_classes).astype(int),
                            0, cfg.num_classes - 1)
            gp.append(grade)
        st.append(batch["score"].numpy())
        gt.append(batch["grade"].numpy())
    return (np.concatenate(sp), np.concatenate(gp),
            np.concatenate(st), np.concatenate(gt))
