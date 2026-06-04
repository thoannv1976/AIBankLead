"""Data loading, cleaning and preparation for model training."""

from __future__ import annotations

import re
from io import BytesIO

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from . import config


def _norm_key(name: str) -> str:
    """Normalize a column header to a comparison key (lowercase, alnum only)."""
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to canonical names using the alias table."""
    rename = {}
    for col in df.columns:
        key = _norm_key(col)
        if key in config.COLUMN_ALIASES:
            rename[col] = config.COLUMN_ALIASES[key]
    return df.rename(columns=rename)


def load_csv(file_or_buffer) -> pd.DataFrame:
    """Read a CSV file/buffer and standardize the column names."""
    df = pd.read_csv(file_or_buffer)
    return standardize_columns(df)


def data_overview(df: pd.DataFrame) -> dict:
    """Build a summary dict used by the Upload & Preview page."""
    n_rows, n_cols = df.shape
    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    overview = {
        "n_rows": n_rows,
        "n_cols": n_cols,
        "missing_total": int(df.isna().sum().sum()),
        "missing_by_col": missing,
        "has_target": config.TARGET in df.columns,
    }

    if config.TARGET in df.columns:
        target = df[config.TARGET]
        counts = target.value_counts(dropna=False).sort_index()
        accept = int((target == 1).sum())
        total = int(target.notna().sum())
        overview["target_counts"] = counts
        overview["acceptance_rate"] = (accept / total) if total else 0.0
        overview["n_accepted"] = accept
    return overview


def find_id_column(df: pd.DataFrame) -> pd.Series:
    """Return a customer-id series (uses ID column if present, else a range)."""
    if "ID" in df.columns:
        return df["ID"].reset_index(drop=True)
    return pd.Series(range(1, len(df) + 1), name="ID")


def preprocess(df: pd.DataFrame, test_size: float = 0.25, random_state: int = 42):
    """Clean data and produce train/test splits for tree and scaled models.

    Steps:
      * drop non-predictive columns (ID, ZIP Code, ...)
      * fix negative Experience values
      * coerce numerics and median-impute any remaining missing values
      * separate features / target
      * stratified train/test split
      * standard-scale a copy of the features for Logistic Regression
    """
    if config.TARGET not in df.columns:
        raise ValueError(
            f"Target column '{config.TARGET}' not found. "
            "Please make sure the dataset contains a personal-loan label."
        )

    work = df.copy()

    # Keep a customer id aligned with the rows before we drop it.
    ids = find_id_column(work)

    # 1. Drop non-predictive columns.
    drop_now = [c for c in config.DROP_COLUMNS if c in work.columns]
    work = work.drop(columns=drop_now)

    # 2. Fix negative experience values (data-entry artefact in this dataset).
    if "Experience" in work.columns:
        work["Experience"] = work["Experience"].abs()

    # 3. Drop rows with a missing target, then split X / y.
    work = work[work[config.TARGET].notna()].copy()
    ids = ids.loc[work.index].reset_index(drop=True)
    work = work.reset_index(drop=True)

    y = work[config.TARGET].astype(int)
    X = work.drop(columns=[config.TARGET])

    # 4. Coerce to numeric and median-impute remaining gaps.
    X = X.apply(pd.to_numeric, errors="coerce")
    medians = X.median(numeric_only=True)
    X = X.fillna(medians)

    feature_names = list(X.columns)

    # 5. Stratified split (preserves class imbalance in both folds).
    stratify = y if y.nunique() > 1 else None
    idx = np.arange(len(X))
    (X_train, X_test, y_train, y_test, idx_train, idx_test) = train_test_split(
        X, y, idx, test_size=test_size, random_state=random_state, stratify=stratify
    )

    # 6. Scaled copies for Logistic Regression.
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train), columns=feature_names, index=X_train.index
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test), columns=feature_names, index=X_test.index
    )

    return {
        "X": X,
        "y": y,
        "ids": ids,
        "feature_names": feature_names,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "X_train_scaled": X_train_scaled,
        "X_test_scaled": X_test_scaled,
        "scaler": scaler,
        "medians": medians,
        "dropped_columns": drop_now,
        "test_index": idx_test,
        "n_train": len(X_train),
        "n_test": len(X_test),
    }


def to_excel_bytes(df: pd.DataFrame, sheet_name: str = "Leads") -> bytes:
    """Serialize a DataFrame to an .xlsx byte buffer for download."""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return buffer.getvalue()
