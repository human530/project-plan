"""評估指標（對應 docs/04）。

核心主張：一致性要用 ICC(2,1) + Bland–Altman，而不是只看 Pearson 相關
（相關高 ≠ 一致）。所有主要指標都附 bootstrap 95% 信賴區間。
"""
from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
from scipy import stats
from sklearn.metrics import cohen_kappa_score, accuracy_score, confusion_matrix


def icc_2_1(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """ICC(2,1)：雙向隨機、單一評分者、絕對一致性。

    把 (專家分數, 模型分數) 視為對同一受試者的兩位評分者，計算絕對一致性 ICC。
    """
    ratings = np.column_stack([y_true, y_pred]).astype(np.float64)
    n, k = ratings.shape                      # n 受試者, k=2 評分者
    grand = ratings.mean()
    row_means = ratings.mean(axis=1)
    col_means = ratings.mean(axis=0)

    ss_total = ((ratings - grand) ** 2).sum()
    ss_row = k * ((row_means - grand) ** 2).sum()
    ss_col = n * ((col_means - grand) ** 2).sum()
    ss_err = ss_total - ss_row - ss_col

    df_row = n - 1
    df_col = k - 1
    df_err = df_row * df_col
    if df_err <= 0 or df_row <= 0:
        return float("nan")

    msr = ss_row / df_row
    msc = ss_col / df_col
    mse = ss_err / df_err

    denom = msr + (k - 1) * mse + k * (msc - mse) / n
    if denom == 0:
        return float("nan")
    return float((msr - mse) / denom)


@dataclass
class BlandAltman:
    bias: float            # 平均差（系統性偏誤）
    sd_diff: float         # 差的標準差
    loa_lower: float       # 一致性下限 bias - 1.96*sd
    loa_upper: float       # 一致性上限 bias + 1.96*sd


def bland_altman(y_true: np.ndarray, y_pred: np.ndarray) -> BlandAltman:
    diff = y_pred - y_true
    bias = float(diff.mean())
    sd = float(diff.std(ddof=1)) if len(diff) > 1 else 0.0
    return BlandAltman(bias=bias, sd_diff=sd,
                       loa_lower=bias - 1.96 * sd, loa_upper=bias + 1.96 * sd)


def _bootstrap_ci(y_true, y_pred, fn, n_boot=2000, seed=0, alpha=0.05):
    """對任意 metric fn(y_true,y_pred) 做百分位 bootstrap 信賴區間。"""
    rng = np.random.default_rng(seed)
    n = len(y_true)
    stats_arr = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        try:
            stats_arr.append(fn(y_true[idx], y_pred[idx]))
        except Exception:
            continue
    if not stats_arr:
        return (float("nan"), float("nan"))
    lo = float(np.percentile(stats_arr, 100 * alpha / 2))
    hi = float(np.percentile(stats_arr, 100 * (1 - alpha / 2)))
    return (lo, hi)


def regression_report(y_true: np.ndarray, y_pred: np.ndarray, n_boot: int = 1000, seed: int = 0):
    """連續分數的一致性報告：ICC、Bland–Altman、Pearson/Spearman、RMSE、MAE（皆附 95% CI）。"""
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)

    def rmse(a, b):
        return float(np.sqrt(np.mean((a - b) ** 2)))

    def mae(a, b):
        return float(np.mean(np.abs(a - b)))

    def pearson(a, b):
        if np.std(a) == 0 or np.std(b) == 0:
            return float("nan")
        return float(stats.pearsonr(a, b)[0])

    def spearman(a, b):
        return float(stats.spearmanr(a, b)[0])

    ba = bland_altman(y_true, y_pred)
    pear_r = pearson(y_true, y_pred)
    pear_p = float(stats.pearsonr(y_true, y_pred)[1]) if np.std(y_true) and np.std(y_pred) else float("nan")

    return {
        "n": int(len(y_true)),
        "icc_2_1": icc_2_1(y_true, y_pred),
        "icc_2_1_ci95": _bootstrap_ci(y_true, y_pred, icc_2_1, n_boot, seed),
        "pearson_r": pear_r,
        "pearson_p": pear_p,
        "pearson_ci95": _bootstrap_ci(y_true, y_pred, pearson, n_boot, seed),
        "spearman_r": spearman(y_true, y_pred),
        "rmse": rmse(y_true, y_pred),
        "rmse_ci95": _bootstrap_ci(y_true, y_pred, rmse, n_boot, seed),
        "mae": mae(y_true, y_pred),
        "bland_altman": asdict(ba),
    }


def classification_report(y_true: np.ndarray, y_pred: np.ndarray, num_classes: int):
    """嚴重度分級報告：accuracy、Quadratic Weighted Kappa、混淆矩陣。

    QWK 對「有序 + 不平衡」比單純 accuracy 更合適（對應 docs/04）。
    """
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    labels = list(range(num_classes))
    qwk = float(cohen_kappa_score(y_true, y_pred, weights="quadratic", labels=labels))
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "quadratic_weighted_kappa": qwk,
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=labels).tolist(),
    }
