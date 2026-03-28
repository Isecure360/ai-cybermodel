"""
📍 app/services/predictor.py

Responsibilities:
- Loads the active model & features via the ModelLoader singleton
- Handles single models and ensemble/hybrid models
- Extracts URL features
- Returns prediction, probability, and base-model breakdown (if ensemble)
- Provides helper to fetch active model metrics for /model-info endpoint
"""

import os
import json
import pandas as pd
from typing import Dict, Any
from app.services.model_loader import model_loader
from app.services.feature_engineering import extract_features_from_url

# =========================
# PREDICTION
# =========================
def predict_url(url: str) -> Dict[str, Any]:
    """
    Predict if a URL is phishing or legit.
    Returns prediction, probability, and optional breakdown for ensemble models.
    """
    model = model_loader.load_model()
    feature_columns = model_loader.load_features()
    
    # Extract features
    features = extract_features_from_url(url)

    # Align features with trained columns
    df = pd.DataFrame([features])
    df = df.reindex(columns=feature_columns, fill_value=0)

    # Base prediction
    if not hasattr(model, "predict"):
        raise ValueError("Active model cannot predict. Invalid model type.")

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df).max() if hasattr(model, "predict_proba") else None

    # Optional: per-model probabilities if ensemble has base_models attribute
    base_model_probs = {}
    if hasattr(model, "base_models"):
        for name, m in model.base_models.items():
            try:
                base_pred_prob = m.predict_proba(df).max()
            except AttributeError:
                base_pred_prob = None
            base_model_probs[name] = float(base_pred_prob) if base_pred_prob is not None else None

    return {
        "url": url,
        "prediction": int(prediction),
        "probability": float(probability) if probability is not None else None,
        "base_model_probs": base_model_probs if base_model_probs else None
    }

# =========================
# HELPER FOR /MODEL-INFO
# =========================
def get_active_model_info() -> Dict[str, Any]:
    """
    Returns active model metadata including metrics and base models.
    Used for /model-info endpoint.
    """
    metadata = model_loader.get_model_metadata()
    model_folder = os.path.join("models", metadata["active_model"].replace(".pkl", "_results_*"))

    # Fetch metrics.json from the folder
    # If multiple folders exist, pick latest by timestamp
    import glob
    folders = sorted(glob.glob(model_folder), reverse=True)
    metrics = {}
    if folders:
        metrics_file = os.path.join(folders[0], "metrics.json")
        if os.path.exists(metrics_file):
            with open(metrics_file, "r") as f:
                metrics = json.load(f)

    base_models = getattr(model_loader.model, "base_models", None)
    if base_models:
        base_models_list = list(base_models.keys())
    else:
        base_models_list = None

    return {
        "active_model": metadata["active_model"],
        "model_type": metadata["model_type"],
        "version": metadata["version"],
        "metrics": metrics,
        "base_models": base_models_list
    }

# =========================
# QUICK TEST
# =========================
if __name__ == "__main__":
    test_url = "http://secure-login-paypal.xyz/login"
    result = predict_url(test_url)
    print("Prediction result:", result)

    info = get_active_model_info()
    print("\nActive model info:", info)