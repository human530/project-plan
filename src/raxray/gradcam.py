"""Grad-CAM 與其「量化」評估（對應 docs/04：不只貼圖，要量化熱區是否落在關節區域）。

自寫的最小 Grad-CAM：對目標卷積層掛 forward/backward hook，取得啟動與梯度，
加權後得到熱區圖。再用 joint_boxes 計算「熱區能量落在關節框內的比例」(energy ratio)，
作為可解釋性的量化指標——對照「隨機熱區基準」才有意義。
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn.functional as F


class GradCAM:
    def __init__(self, model, target_layer_name: str):
        self.model = model
        self.activations = None
        self.gradients = None
        layer = self._find_layer(target_layer_name)
        layer.register_forward_hook(self._fwd_hook)
        layer.register_full_backward_hook(self._bwd_hook)

    def _find_layer(self, name: str):
        # name 可為 "layer4" 或 "features"，於 backbone 子模組中尋找
        module = self.model.backbone
        if hasattr(module, name):
            return getattr(module, name)
        for n, m in module.named_modules():
            if n.endswith(name):
                return m
        raise ValueError(f"找不到目標層：{name}")

    def _fwd_hook(self, module, inp, out):
        self.activations = out.detach()

    def _bwd_hook(self, module, grad_in, grad_out):
        self.gradients = grad_out[0].detach()

    def __call__(self, x: torch.Tensor, scalar_fn) -> np.ndarray:
        """x: (1,3,H,W)。scalar_fn(logits)->純量，作為反傳目標。回傳 (H,W) 正規化熱區圖。"""
        self.model.zero_grad()
        logits = self.model(x)
        score = scalar_fn(logits)
        score.backward()

        grads = self.gradients              # (1,C,h,w)
        acts = self.activations             # (1,C,h,w)
        weights = grads.mean(dim=(2, 3), keepdim=True)
        raw = (weights * acts).sum(dim=1, keepdim=True)
        cam = F.relu(raw)
        # 退化保護：若正向 CAM 整片為零（ReLU 全裁掉），改用權重×啟動的絕對量值，
        # 仍能反映「模型對哪些區域敏感」，避免量化指標變成無意義的 0。
        if float(cam.max()) <= 0:
            cam = raw.abs()
        cam = F.interpolate(cam, size=x.shape[2:], mode="bilinear", align_corners=False)
        cam = cam[0, 0].cpu().numpy()
        if cam.max() > cam.min():
            cam = (cam - cam.min()) / (cam.max() - cam.min())
        return cam


def energy_in_boxes(cam: np.ndarray, boxes: np.ndarray) -> float:
    """熱區能量落在關節框內的比例（0~1）。boxes: (J,4) [x0,y0,x1,y1] 像素座標。"""
    total = cam.sum()
    if total <= 0:
        return 0.0
    mask = np.zeros_like(cam, dtype=bool)
    h, w = cam.shape
    for x0, y0, x1, y1 in boxes.astype(int):
        x0, x1 = max(0, x0), min(w, x1)
        y0, y1 = max(0, y0), min(h, y1)
        if x1 > x0 and y1 > y0:
            mask[y0:y1, x0:x1] = True
    return float(cam[mask].sum() / total)
