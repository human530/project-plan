"""CORN 序數迴歸損失與解碼（對應 docs/03：MVP 保底用序數分級而非硬回歸總分）。

SvH 嚴重度本質是「有序」（正常 < 輕 < 中 < 重），用一般分類會忽略順序、
用一般回歸在大分數範圍又難收斂。CORN（Cao et al., 2020）把 K 級序數問題拆成
K-1 個「條件式」二元判斷 P(y>k | y>k-1)，兼顧順序性與穩定性。

參考：Cao, Mirjalili & Raschka (2020), "Rank consistent ordinal regression
for neural networks with application to age estimation"（CORN）。
本實作為自寫版本，介面簡單、可獨立驗證。
"""
from __future__ import annotations

import torch
import torch.nn.functional as F


def corn_loss(logits: torch.Tensor, targets: torch.Tensor, num_classes: int) -> torch.Tensor:
    """CORN 條件式損失。

    logits: (N, K-1) 每個門檻一個 logit。
    targets: (N,) 整數等級 0..K-1。
    """
    num_tasks = num_classes - 1
    total = logits.new_zeros(())
    count = 0
    for k in range(num_tasks):
        # 第 k 個門檻：只在「y >= k」的樣本上訓練條件機率 P(y>k | y>=k)
        mask = targets >= k
        if mask.sum() == 0:
            continue
        logit_k = logits[mask, k]
        target_k = (targets[mask] > k).float()
        total = total + F.binary_cross_entropy_with_logits(logit_k, target_k, reduction="sum")
        count += int(mask.sum().item())
    if count == 0:
        return logits.new_zeros(()).requires_grad_(True)
    return total / count


def corn_cumulative_probs(logits: torch.Tensor) -> torch.Tensor:
    """把 (N,K-1) logits 轉成各門檻的累積機率 P(y>k) = ∏_{j<=k} sigmoid(logit_j)。"""
    probs = torch.sigmoid(logits)
    return torch.cumprod(probs, dim=1)


def corn_predict_label(logits: torch.Tensor) -> torch.Tensor:
    """硬預測等級 = 累積機率 > 0.5 的門檻數量。"""
    cum = corn_cumulative_probs(logits)
    return (cum > 0.5).sum(dim=1)


def corn_expected_rank(logits: torch.Tensor) -> torch.Tensor:
    """軟預測（連續）等級 = 累積機率之和，落在 [0, K-1]。

    這個連續值可再線性映射回 SvH 分數尺度，供 ICC / Bland–Altman 等一致性分析使用。
    """
    cum = corn_cumulative_probs(logits)
    return cum.sum(dim=1)
