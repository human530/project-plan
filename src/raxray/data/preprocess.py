"""影像前處理管線（對應 docs/02 §前處理）。

提供 X 光常用的 window-level、對比增強、尺寸標準化與正規化。
為了讓 smoke test 不依賴 OpenCV，這裡用 numpy/PIL 實作一個輕量版；
在 Colab 上可改用 OpenCV 的 cv2.createCLAHE 取得更佳的 CLAHE 效果。
"""
from __future__ import annotations

import numpy as np
from PIL import Image


def window_level(img: np.ndarray, low_pct: float = 1.0, high_pct: float = 99.0) -> np.ndarray:
    """以百分位裁切動態範圍（模擬放射 window/level），壓掉極端值後線性拉伸到 0~1。"""
    lo, hi = np.percentile(img, [low_pct, high_pct])
    if hi <= lo:
        hi = lo + 1e-6
    out = (img - lo) / (hi - lo)
    return np.clip(out, 0.0, 1.0).astype(np.float32)


def equalize_contrast(img: np.ndarray) -> np.ndarray:
    """簡易直方圖均衡化（CLAHE 的輕量替代）。img 為 0~1 float。"""
    flat = (img * 255).astype(np.uint8).ravel()
    hist = np.bincount(flat, minlength=256)
    cdf = hist.cumsum().astype(np.float64)
    cdf_masked = np.ma.masked_equal(cdf, 0)
    if cdf_masked.count() == 0:
        return img
    cdf_norm = (cdf_masked - cdf_masked.min()) / (cdf_masked.max() - cdf_masked.min())
    cdf_filled = np.ma.filled(cdf_norm, 0)
    eq = cdf_filled[(img * 255).astype(np.uint8)]
    return eq.astype(np.float32)


def resize(img: np.ndarray, size: int) -> np.ndarray:
    """雙線性縮放到 size x size。"""
    pil = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    pil = pil.resize((size, size), Image.BILINEAR)
    return np.asarray(pil).astype(np.float32) / 255.0


# ImageNet 預訓練統計（灰階複製成 3 通道後使用）
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def to_model_tensor(img: np.ndarray, size: int, use_clahe: bool = True):
    """完整前處理：window-level → (對比增強) → resize → 灰階轉 3 通道 → ImageNet 正規化。

    回傳 shape (3, size, size) 的 float32 numpy（再由 Dataset 轉成 torch tensor）。
    """
    x = window_level(img)
    if use_clahe:
        x = equalize_contrast(x)
    x = resize(x, size)
    x = np.stack([x, x, x], axis=0)          # (3,H,W) 灰階複製
    x = (x - IMAGENET_MEAN[:, None, None]) / IMAGENET_STD[:, None, None]
    return x.astype(np.float32)


def augment(img: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """輕量資料增強（對應 docs/02：旋轉/翻轉/亮度），只用 numpy。"""
    if rng.random() < 0.5:
        img = np.fliplr(img).copy()
    k = int(rng.integers(0, 4))
    if k:
        img = np.rot90(img, k=k).copy()        # 90 度倍數旋轉，避免引入黑邊
    if rng.random() < 0.5:
        img = np.clip(img * rng.uniform(0.85, 1.15), 0, 1)
    return img.astype(np.float32)
