# src/data/ingest.py

# Step A — Load ALL datasets

import os
import pandas as pd

RAW_DIR = "data/raw"

def load_all_datasets():
    dfs = []
    for file in os.listdir(RAW_DIR):
        if file.endswith(".csv"):
            path = os.path.join(RAW_DIR, file)
            df = pd.read_csv(path)
            dfs.append(df)
    return dfs

# Step B — Detect URL column (heuristic)

def detect_url_column(df):
    for col in df.columns:
        if df[col].astype(str).str.contains("http", na=False).mean() > 0.5:
            return col
    return None


# Step C — Create canonical dataset
def create_base_dataframe(feature_columns):
    import pandas as pd
    return pd.DataFrame(columns=feature_columns + ["label"])

# Step D — Transform each dataset
from src.features.url_features import extract_features_from_url
import random

def transform_dataset(df, feature_columns):
    url_col = detect_url_column(df)

    if not url_col:
        return None

    records = []

    for _, row in df.iterrows():
        url = row[url_col]

        features = extract_features_from_url(url)

        # merge with label if exists
        label = row.get("label", None)

        features["label"] = label
        records.append(features)

    return records
# Step E — Merge everything
def build_unified_dataset(dfs, feature_columns):
    base_df = create_base_dataframe(feature_columns)

    all_records = []

    for df in dfs:
        transformed = transform_dataset(df, feature_columns)
        if transformed:
            all_records.extend(transformed)

    import pandas as pd
    return pd.DataFrame(all_records)
# 
#