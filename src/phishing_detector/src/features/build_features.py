from src.features.url_features import extract_features_from_url
import pandas as pd

def build_features(df):
    feature_list = df["url"].apply(extract_features_from_url)


    X = pd.DataFrame(feature_list.tolist())
    y = df["label"]

    return X, y, X.columns.tolist()