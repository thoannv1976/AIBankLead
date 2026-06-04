"""Model training with class-imbalance handling and feature importances."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from . import metrics

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except Exception:  # pragma: no cover - environment without xgboost
    HAS_XGB = False


def _scale_pos_weight(y) -> float:
    """scale_pos_weight = negatives / positives, for XGBoost imbalance."""
    y = np.asarray(y)
    pos = max(1, int((y == 1).sum()))
    neg = int((y == 0).sum())
    return neg / pos


def train_logistic_regression(data: dict):
    """Logistic Regression on scaled features with balanced class weights."""
    model = LogisticRegression(
        max_iter=2000, class_weight="balanced", solver="liblinear"
    )
    model.fit(data["X_train_scaled"], data["y_train"])
    return model


def train_random_forest(data: dict):
    """Random Forest on raw features with balanced class weights."""
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(data["X_train"], data["y_train"])
    return model


def train_xgboost(data: dict):
    """XGBoost on raw features with scale_pos_weight for imbalance."""
    model = XGBClassifier(
        n_estimators=400,
        max_depth=4,
        learning_rate=0.08,
        subsample=0.9,
        colsample_bytree=0.9,
        scale_pos_weight=_scale_pos_weight(data["y_train"]),
        eval_metric="aucpr",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(data["X_train"], data["y_train"])
    return model


def _uses_scaled(model_name: str) -> bool:
    return model_name == "Logistic Regression"


def _predict_proba(model, X) -> np.ndarray:
    return model.predict_proba(X)[:, 1]


def train_model(model_name: str, data: dict):
    """Train one model by name and return (model, test_scores, metrics)."""
    if model_name == "Logistic Regression":
        model = train_logistic_regression(data)
        X_test = data["X_test_scaled"]
    elif model_name == "Random Forest":
        model = train_random_forest(data)
        X_test = data["X_test"]
    elif model_name == "XGBoost":
        if not HAS_XGB:
            raise RuntimeError("xgboost is not installed in this environment.")
        model = train_xgboost(data)
        X_test = data["X_test"]
    else:
        raise ValueError(f"Unknown model: {model_name}")

    y_score = _predict_proba(model, X_test)
    y_pred = (y_score >= 0.5).astype(int)
    result = metrics.evaluate(data["y_test"], y_pred, y_score)
    return model, y_score, result


def train_all(data: dict, model_names: list[str]):
    """Train several models; returns dict of models and metrics table."""
    models = {}
    test_scores = {}
    results = {}
    for name in model_names:
        if name == "XGBoost" and not HAS_XGB:
            continue
        model, y_score, result = train_model(name, data)
        models[name] = model
        test_scores[name] = y_score
        results[name] = result
    return models, test_scores, results


def feature_importance(model, model_name: str, feature_names: list[str]) -> pd.DataFrame:
    """Return a tidy importance table for any of the supported models.

    Tree models expose `feature_importances_`; Logistic Regression exposes
    signed coefficients (direction + relative magnitude).
    """
    if model_name == "Logistic Regression":
        coefs = model.coef_[0]
        df = pd.DataFrame({
            "feature": feature_names,
            "coefficient": coefs,
            "importance": np.abs(coefs),
            "direction": np.where(coefs >= 0, "increases", "decreases"),
        })
        return df.sort_values("importance", ascending=False).reset_index(drop=True)

    importances = getattr(model, "feature_importances_", None)
    if importances is None:
        return pd.DataFrame({"feature": feature_names, "importance": np.nan})
    df = pd.DataFrame({"feature": feature_names, "importance": importances})
    return df.sort_values("importance", ascending=False).reset_index(drop=True)


def score_all_customers(model, model_name: str, data: dict) -> np.ndarray:
    """Predict acceptance probability for every customer in the dataset."""
    if _uses_scaled(model_name):
        X_all = pd.DataFrame(
            data["scaler"].transform(data["X"]),
            columns=data["feature_names"],
            index=data["X"].index,
        )
    else:
        X_all = data["X"]
    return _predict_proba(model, X_all)
