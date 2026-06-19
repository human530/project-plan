"""合成「類手部 X 光」資料產生器。

用途：在真實資料集（RA2 DREAM 需申請）到位前，先用結構化合成資料把整條管線
（前處理 → 訓練 → 評估 → Grad-CAM）端到端跑通並驗證正確性。

設計重點，讓 smoke test 有意義（而非純雜訊）：
- 每張影像在數個「關節位置」放上亮斑（模擬掌指/近端指間關節）。
- 損傷越重，關節區域的對比/侵蝕紋理越明顯——使「損傷分數」與影像特徵真的相關，
  讓模型學得到東西、Grad-CAM 也能落在關節區域。
- 以 patient_id 分組（同一病人多張），用來驗證「病人層級切分、不可跨集」。

⚠️ 這只是工程驗證用的假資料，不具任何臨床意義。
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


# 模擬關節中心（相對座標，0~1），約略對應一隻手的數個關節
JOINT_CENTERS = [
    (0.30, 0.35), (0.45, 0.28), (0.60, 0.30), (0.72, 0.38),  # MCP 一排
    (0.32, 0.55), (0.46, 0.50), (0.60, 0.52), (0.70, 0.58),  # PIP 一排
]


@dataclass
class SyntheticSample:
    image: np.ndarray     # (H, W) float32, 0~1
    score: float          # 連續 SvH 風格總分（0 ~ score_max）
    grade: int            # 嚴重度等級（0..num_classes-1）
    patient_id: str
    joint_boxes: np.ndarray  # (J, 4) [x0,y0,x1,y1] 像素座標，供 Grad-CAM 量化用


def _draw_joint(img: np.ndarray, cx: int, cy: int, radius: int,
                severity: float, rng: np.random.Generator) -> None:
    """在 (cx,cy) 畫一個關節亮斑；severity 越高，關節結構越弱（變暗）且侵蝕暗紋越多。

    讓「損傷分數」與關節區域影像特徵呈清楚的單調關係，使遷移學習模型學得到、
    Grad-CAM 也能落在關節區域（模擬臨床上侵蝕/間隙狹窄造成的結構流失）。
    """
    h, w = img.shape
    y0, y1 = max(0, cy - radius), min(h, cy + radius)
    x0, x1 = max(0, cx - radius), min(w, cx + radius)
    yy, xx = np.mgrid[y0:y1, x0:x1]
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    # 關節亮度隨 severity 下降（結構流失）：健康關節亮、嚴重關節暗
    intensity = 0.7 * (1.0 - 0.7 * severity)
    blob = np.clip(1.0 - dist / radius, 0, 1) * intensity
    img[y0:y1, x0:x1] += blob
    # 侵蝕：在關節邊緣挖暗點，數量隨 severity 增加
    n_erosion = int(severity * 8)
    for _ in range(n_erosion):
        ex = rng.integers(x0, max(x0 + 1, x1))
        ey = rng.integers(y0, max(y0 + 1, y1))
        rr = max(1, radius // 4)
        ey0, ey1 = max(0, ey - rr), min(h, ey + rr)
        ex0, ex1 = max(0, ex - rr), min(w, ex + rr)
        img[ey0:ey1, ex0:ex1] *= 0.4


def generate_dataset(n_patients: int = 40, imgs_per_patient: int = 2,
                     image_size: int = 224, num_classes: int = 4,
                     score_max: float = 448.0, seed: int = 0):
    """產生一批合成樣本（list[SyntheticSample]）。"""
    rng = np.random.default_rng(seed)
    samples: list[SyntheticSample] = []
    size = image_size

    for p in range(n_patients):
        pid = f"P{p:04d}"
        # 病人層級的「基礎疾病程度」，使同病人的影像彼此相關（模擬真實情境）
        base_sev = rng.uniform(0.0, 1.0)
        for k in range(imgs_per_patient):
            sev = float(np.clip(base_sev + rng.normal(0, 0.08), 0, 1))
            img = rng.normal(0.25, 0.04, size=(size, size)).astype(np.float32)
            img = np.clip(img, 0, 1)
            radius = max(6, size // 14)
            boxes = []
            for (rx, ry) in JOINT_CENTERS:
                cx = int(rx * size + rng.integers(-2, 3))
                cy = int(ry * size + rng.integers(-2, 3))
                _draw_joint(img, cx, cy, radius, sev, rng)
                boxes.append([cx - radius, cy - radius, cx + radius, cy + radius])
            img = np.clip(img, 0, 1)

            score = float(sev * score_max * rng.uniform(0.9, 1.0))
            grade = int(min(num_classes - 1, int(sev * num_classes)))
            samples.append(SyntheticSample(
                image=img, score=score, grade=grade, patient_id=pid,
                joint_boxes=np.array(boxes, dtype=np.float32),
            ))
    rng.shuffle(samples)
    return samples
