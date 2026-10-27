"""Diebold-Mariano test (Newey-West HAC variance) and Holm correction."""

from __future__ import annotations

import numpy as np
from scipy import stats

from trafficml.data.masking import valid_mask


def loss_differential(y_true: np.ndarray, pred_a: np.ndarray, pred_b: np.ndarray) -> np.ndarray:
    """d_t = mean over sensors of |e_a| - |e_b| at one horizon; y_true and preds are (S, N).

    Only points scored for both models (valid y_true) count; anchors with none are dropped.
    """
    if y_true.shape != pred_a.shape or y_true.shape != pred_b.shape or y_true.ndim != 2:
        raise ValueError("expected equal (samples, sensors) shapes")
    valid = valid_mask(y_true)
    if not (np.isfinite(pred_a[valid]).all() and np.isfinite(pred_b[valid]).all()):
        raise ValueError("non-finite predictions on scored points")
    diff = np.abs(pred_a - y_true) - np.abs(pred_b - y_true)
    counts = valid.sum(axis=1)
    d = np.where(valid, diff, 0).sum(axis=1) / np.maximum(counts, 1)
    return d[counts > 0]


def newey_west_variance(d: np.ndarray, lag: int) -> float:
    """Long-run variance of the mean-centred series with Bartlett weights."""
    e = d - d.mean()
    t = len(e)
    var = e @ e / t
    for k in range(1, lag + 1):
        var += 2 * (1 - k / (lag + 1)) * (e[k:] @ e[:-k]) / t
    return float(var)


def diebold_mariano(d: np.ndarray, h: int) -> dict[str, float]:
    """Two-sided DM test of E[d_t] = 0 for horizon h (in steps).

    HAC lag is max(h - 1, Newey-West rule-of-thumb 4(T/100)^(2/9)): overlapping h-step
    forecasts give MA(h-1) errors, and traffic errors persist longer than that.
    A positive statistic means model b has lower absolute error.
    """
    d = np.asarray(d, dtype=float)
    t = len(d)
    if d.ndim != 1 or t < 3 or not np.isfinite(d).all() or not 1 <= h < t:
        raise ValueError("DM needs a finite series and 1 <= horizon < sample count")
    lag = max(h - 1, int(np.floor(4 * (t / 100) ** (2 / 9))))
    lag = min(lag, t - 1)
    var = newey_west_variance(d, lag)
    if not np.isfinite(var) or var <= 0:
        return {
            "mean_diff": float(d.mean()),
            "dm_stat": float("nan"),
            "p_value": float("nan"),
            "lag": lag,
        }
    stat = d.mean() / np.sqrt(var / t)
    p = 2 * stats.norm.sf(abs(stat))
    return {"mean_diff": float(d.mean()), "dm_stat": float(stat), "p_value": float(p), "lag": lag}


def holm(p_values) -> np.ndarray:
    """Holm-Bonferroni adjusted p-values (same order as the input)."""
    p = np.asarray(p_values, dtype=float)
    finite = np.isfinite(p)
    if np.any((p[finite] < 0) | (p[finite] > 1)):
        raise ValueError("p-values must be between zero and one")
    if not finite.all():
        # Undefined tests stay undefined and count toward the declared family size.
        safe = np.where(finite, p, 1.0)
        adjusted = holm(safe)
        return np.where(finite, adjusted, np.nan)
    order = np.argsort(p)
    m = len(p)
    adjusted = np.maximum.accumulate((m - np.arange(m)) * p[order])
    out = np.empty(m)
    out[order] = np.minimum(adjusted, 1.0)
    return out
