"""PyTorch Dataset 與「病人層級切分」（對應 docs/02 §資料切分、docs/04 §防資料外洩）。

核心紀律：同一個病人的所有影像，必須整組落在同一個子集（train/val/test），
絕不可跨集，否則會造成資料外洩、嚴重高估準確度。split_by_patient 內含 assert 檢查。
"""
from __future__ import annotations

from typing import Sequence

import numpy as np
import torch
from torch.utils.data import Dataset

from .preprocess import to_model_tensor, augment
from .synthetic import SyntheticSample


def split_by_patient(samples: Sequence[SyntheticSample], val_frac: float,
                     test_frac: float, seed: int = 0):
    """依 patient_id 分組後切分，回傳 (train, val, test) 三個 list。

    回傳前會 assert 三個子集的病人集合「兩兩不相交」，確保無資料外洩。
    """
    pids = sorted({s.patient_id for s in samples})
    rng = np.random.default_rng(seed)
    rng.shuffle(pids)

    n = len(pids)
    n_test = max(1, int(round(n * test_frac)))
    n_val = max(1, int(round(n * val_frac)))
    test_pids = set(pids[:n_test])
    val_pids = set(pids[n_test:n_test + n_val])
    train_pids = set(pids[n_test + n_val:])

    # 防資料外洩：三組病人不可重疊
    assert train_pids.isdisjoint(val_pids), "train/val 病人重疊！"
    assert train_pids.isdisjoint(test_pids), "train/test 病人重疊！"
    assert val_pids.isdisjoint(test_pids), "val/test 病人重疊！"

    def pick(pset):
        return [s for s in samples if s.patient_id in pset]

    return pick(train_pids), pick(val_pids), pick(test_pids)


class HandXrayDataset(Dataset):
    """把合成（或真實）樣本包成 PyTorch Dataset。

    回傳 dict：image (3,H,W) tensor、score (float)、grade (long)、
    patient_id、joint_boxes（Grad-CAM 量化用）。
    """

    def __init__(self, samples: Sequence[SyntheticSample], image_size: int,
                 train: bool = False, use_clahe: bool = True, seed: int = 0):
        self.samples = list(samples)
        self.image_size = image_size
        self.train = train
        self.use_clahe = use_clahe
        self.rng = np.random.default_rng(seed)

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int):
        s = self.samples[idx]
        img = s.image
        if self.train:
            img = augment(img, self.rng)
        x = to_model_tensor(img, self.image_size, use_clahe=self.use_clahe)
        return {
            "image": torch.from_numpy(x),
            "score": torch.tensor(s.score, dtype=torch.float32),
            "grade": torch.tensor(s.grade, dtype=torch.long),
            "patient_id": s.patient_id,
            "joint_boxes": torch.from_numpy(s.joint_boxes),
        }
