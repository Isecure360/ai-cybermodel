# src/phishing_detector/io/dataset.py

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


# -------------------------
# Defaults for PhiUSIIL
# -------------------------
DEFAULT_TARGET_COL = "label"
DEFAULT_DROP_COLS = ["FILENAME"]

# Common “semantic” columns in PhiUSIIL. We keep them (unless user opts out).
DEFAULT_TEXT_COL_CANDIDATES = ["Title"]
DEFAULT_URL_COL_CANDIDATES = ["URL"]
DEFAULT_CATEGORICAL_COL_CANDIDATES = ["Domain", "TLD"]


@dataclass(frozen=True)
class DatasetMetadata:
    path: str
    n_rows_raw: int
    n_rows_after_clean: int
    n_cols_raw: int
    n_cols_after_clean: int
    target_col: str
    dropped_columns: List[str]
    dropped_rows_missing_target: int
    numeric_features: List[str]
    categorical_features: List[str]
    text_features: List[str]
    url_features: List[str]
    # extra info for debugging / EDA
    dtypes: Dict[str, str]
    missing_by_col_top: List[Tuple[str, int]]  # top missing columns
    class_distribution: Dict[Any, int]


def load_phiusiil_csv(path: str) -> pd.DataFrame:
    """
    Load PhiUSIIL phishing dataset CSV.
    Minimal responsibility: read CSV and return DataFrame.
    """
    df = pd.read_csv(path)
    return df


def _safe_drop_columns(df: pd.DataFrame, cols: List[str]) -> Tuple[pd.DataFrame, List[str]]:
    present = [c for c in cols if c in df.columns]
    if not present:
        return df, []
    return df.drop(columns=present), present


def _infer_feature_groups(
    df: pd.DataFrame,
    target_col: str,
    categorical_candidates: Optional[List[str]] = None,
    text_candidates: Optional[List[str]] = None,
    url_candidates: Optional[List[str]] = None,
) -> Tuple[List[str], List[str], List[str], List[str]]:
    """
    Infer feature groups dynamically:
    - Numeric: number dtypes excluding target
    - Categorical: object/category columns OR listed candidates if present
    - Text: text candidates if present (e.g., Title)
    - URL: url candidates if present (e.g., URL)
    """
    categorical_candidates = categorical_candidates or DEFAULT_CATEGORICAL_COL_CANDIDATES
    text_candidates = text_candidates or DEFAULT_TEXT_COL_CANDIDATES
    url_candidates = url_candidates or DEFAULT_URL_COL_CANDIDATES

    # Candidates that actually exist
    cat_present = [c for c in categorical_candidates if c in df.columns and c != target_col]
    text_present = [c for c in text_candidates if c in df.columns and c != target_col]
    url_present = [c for c in url_candidates if c in df.columns and c != target_col]

    # Auto-detect additional categoricals
    auto_cat = df.select_dtypes(include=["object", "category"]).columns.tolist()
    auto_cat = [c for c in auto_cat if c != target_col]

    # Merge and de-dupe (preserving order-ish)
    categorical = []
    for c in cat_present + auto_cat:
        if c not in categorical and c not in text_present and c not in url_present:
            categorical.append(c)

    # Numeric
    numeric = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric = [c for c in numeric if c != target_col]

    return numeric, categorical, text_present, url_present


def prepare_xy(
    df: pd.DataFrame,
    *,
    target_col: str = DEFAULT_TARGET_COL,
    drop_cols: Optional[List[str]] = None,
    drop_missing_target: bool = True,
    # allow overriding candidates if your dataset differs
    categorical_candidates: Optional[List[str]] = None,
    text_candidates: Optional[List[str]] = None,
    url_candidates: Optional[List[str]] = None,
) -> Tuple[pd.DataFrame, pd.Series, DatasetMetadata]:
    """
    Clean and prepare (X, y) with metadata.

    Keeps behavior aligned with your cells:
    - Drop FILENAME if exists
    - Drop rows with NA label (target)
    - Do NOT dropna() on all columns (too destructive)
    - Infer feature types for downstream pipelines
    """
    if target_col not in df.columns:
        raise ValueError(
            f"Target column '{target_col}' not found. Available columns: {df.columns.tolist()}"
        )

    n_rows_raw, n_cols_raw = df.shape
    df_clean = df.copy()

    # Drop known non-feature columns
    drop_cols = drop_cols if drop_cols is not None else DEFAULT_DROP_COLS
    df_clean, dropped_columns = _safe_drop_columns(df_clean, drop_cols)

    # Drop missing target only
    dropped_rows_missing_target = 0
    if drop_missing_target:
        before = len(df_clean)
        df_clean = df_clean.dropna(subset=[target_col])
        dropped_rows_missing_target = before - len(df_clean)

    # Feature groups (dynamic)
    numeric_features, categorical_features, text_features, url_features = _infer_feature_groups(
        df_clean,
        target_col=target_col,
        categorical_candidates=categorical_candidates,
        text_candidates=text_candidates,
        url_candidates=url_candidates,
    )

    # Build X, y
    y = df_clean[target_col].copy()
    X = df_clean.drop(columns=[target_col]).copy()

    # Metadata
    missing_counts = df_clean.isnull().sum().sort_values(ascending=False)
    missing_top = [(idx, int(val)) for idx, val in missing_counts.head(15).items() if int(val) > 0]

    class_dist = y.value_counts(dropna=False).to_dict()

    meta = DatasetMetadata(
        path="(in-memory df)",
        n_rows_raw=n_rows_raw,
        n_rows_after_clean=df_clean.shape[0],
        n_cols_raw=n_cols_raw,
        n_cols_after_clean=df_clean.shape[1],
        target_col=target_col,
        dropped_columns=dropped_columns,
        dropped_rows_missing_target=dropped_rows_missing_target,
        numeric_features=numeric_features,
        categorical_features=categorical_features,
        text_features=text_features,
        url_features=url_features,
        dtypes={c: str(t) for c, t in df_clean.dtypes.items()},
        missing_by_col_top=missing_top,
        class_distribution={k: int(v) for k, v in class_dist.items()},
    )

    return X, y, meta


def split_train_test(
    X: pd.DataFrame,
    y: pd.Series,
    *,
    test_size: float = 0.2,
    random_state: int = 42,
    stratify: bool = True,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Stratified train/test split by default (recommended for imbalanced phishing datasets).
    """
    strat = y if stratify else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=strat
    )
    return X_train, X_test, y_train, y_test


# -------------------------
# Convenience helper (optional)
# -------------------------
def load_prepare_split(
    path: str,
    *,
    target_col: str = DEFAULT_TARGET_COL,
    test_size: float = 0.2,
    random_state: int = 42,
    stratify: bool = True,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, DatasetMetadata]:
    """
    One-liner: load CSV -> prepare X/y -> split.
    """
    df = load_phiusiil_csv(path)
    X, y, meta = prepare_xy(df, target_col=target_col)
    meta = DatasetMetadata(**{**asdict(meta), "path": path})  # set real path
    X_train, X_test, y_train, y_test = split_train_test(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify
    )
    return X_train, X_test, y_train, y_test, meta
