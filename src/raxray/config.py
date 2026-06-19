"""全域設定與隨機種子控制。

本檔集中管理 MVP 訓練/評估的所有超參數，並提供 set_seed 確保可重現
（對應規劃文件 docs/03 的「固定 seed 可重現」與 docs/04 的「可重現紀律」）。
"""
from __future__ import annotations

import os
import random
from dataclasses import dataclass, field, asdict

import numpy as np


@dataclass
class Config:
    # --- 資料 ---
    image_size: int = 224          # 模型輸入邊長；smoke test 會調小
    num_classes: int = 4           # 嚴重度等級數（如 0 正常 / 1 輕 / 2 中 / 3 重）
    score_max: float = 448.0       # SvH 全身總分理論上限（手+腕 erosion+JSN）
    val_frac: float = 0.2
    test_frac: float = 0.2

    # --- 模型 ---
    backbone: str = "resnet18"     # resnet18 | efficientnet_b0
    pretrained: bool = True        # Colab 上用預訓練權重；離線 smoke 可關閉
    head_type: str = "ordinal"     # ordinal(CORN，MVP 保底) | regression

    # --- 訓練 ---
    batch_size: int = 16
    lr: float = 1e-4
    weight_decay: float = 1e-4
    epochs: int = 30
    early_stop_patience: int = 6
    num_workers: int = 2
    amp: bool = False              # 有 GPU 時可開混合精度

    # --- 雜項 ---
    seed: int = 42
    device: str = "auto"           # auto | cpu | cuda
    out_dir: str = "outputs"
    ckpt_name: str = "mvp_best.pt"

    def resolved_device(self) -> str:
        if self.device != "auto":
            return self.device
        try:
            import torch
            return "cuda" if torch.cuda.is_available() else "cpu"
        except Exception:
            return "cpu"

    def to_dict(self) -> dict:
        return asdict(self)


def set_seed(seed: int) -> None:
    """固定所有隨機來源，確保結果可重現。"""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except Exception:
        pass
