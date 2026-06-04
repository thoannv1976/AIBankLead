"""Evaluation metrics, with emphasis on top-k lead-targeting metrics."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def precision_at_k(y_true, y_score, k_fraction: float) -> float:
    """Precision among the top-k fraction of customers ranked by score.

    Mirrors how a marketing team works: sort customers by predicted
    probability, take the top X%, and measure what share actually converted.
    """
    y_true = np.asarray(y_true)
    y_score = np.asarray(y_score)
    n = len(y_true)
    k = max(1, int(round(n * k_fraction)))
    top_idx = np.argsort(y_score)[::-1][:k]
    return float(np.mean(y_true[top_idx]))


def lift_at_k(y_true, y_score, k_fraction: float) -> float:
    """Lift of the top-k fraction vs. the base acceptance rate.

    Lift = (precision among top-k) / (overall positive rate). A lift of 4
    means the targeted group converts 4x better than random outreach.
    """
    y_true = np.asarray(y_true)
    base_rate = float(np.mean(y_true))
    if base_rate == 0:
        return 0.0
    return precision_at_k(y_true, y_score, k_fraction) / base_rate


def evaluate(y_true, y_pred, y_score) -> dict:
    """Compute the full metric panel for a single model."""
    metrics = {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred, zero_division=0),
        "F1-score": f1_score(y_true, y_pred, zero_division=0),
        "ROC-AUC": roc_auc_score(y_true, y_score) if len(set(y_true)) > 1 else float("nan"),
        "PR-AUC": average_precision_score(y_true, y_score) if len(set(y_true)) > 1 else float("nan"),
    }
    for frac, label in [(0.05, "5%"), (0.10, "10%"), (0.20, "20%")]:
        metrics[f"Precision@Top {label}"] = precision_at_k(y_true, y_score, frac)
        metrics[f"Lift@Top {label}"] = lift_at_k(y_true, y_score, frac)
    return metrics


# Metrics that drive "best model" selection for imbalanced lead targeting.
SELECTION_METRICS = ["PR-AUC", "Precision@Top 10%", "Lift@Top 10%"]


def best_model(results: dict) -> str:
    """Pick the strongest model using PR-AUC + top-k lead performance.

    `results` maps model name -> metrics dict. We rank each model on the
    selection metrics and average the ranks; lowest average rank wins.
    """
    if not results:
        return ""
    names = list(results.keys())
    avg_rank = {n: 0.0 for n in names}
    for metric in SELECTION_METRICS:
        scored = sorted(
            names,
            key=lambda n: (results[n].get(metric) if results[n].get(metric) == results[n].get(metric) else -1),
            reverse=True,
        )
        for rank, n in enumerate(scored):
            avg_rank[n] += rank
    return min(avg_rank, key=avg_rank.get)
