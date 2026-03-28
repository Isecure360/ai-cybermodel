"""
📍 app/services/model_loader.py

Centralized model & feature loader.

Responsibilities:
- Loads the active model from models/registry.json
- Loads the associated feature set/vectorizer
- Handles errors gracefully
- Provides helper functions for any service needing the model
"""

import os
import pickle
import json
from typing import Tuple, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "../../models")
REGISTRY_PATH = os.path.join(MODELS_DIR, "registry.json")


class ModelLoaderError(Exception):
    """Custom exception for model loader errors"""
    pass


class ModelLoader:
    def __init__(self):
        self.model = None
        self.feature_columns = None
        self.model_name = None
        self.feature_version = None
        self.model_type = None
        self.version = None
        self._load_registry()

    def _load_registry(self):
        """Load registry.json and assign model metadata"""
        if not os.path.exists(REGISTRY_PATH):
            raise ModelLoaderError("registry.json not found. Promote a model first.")

        with open(REGISTRY_PATH, "r") as f:
            registry = json.load(f)

        self.model_name = registry.get("active_model")
        self.feature_version = registry.get("feature_version")
        self.model_type = registry.get("model_type")
        self.version = registry.get("version")

        if not self.model_name or not self.feature_version:
            raise ModelLoaderError("Registry file is missing required fields.")

    def load_model(self) -> Any:
        """Load the active model"""
        if self.model is not None:
            return self.model  # Already loaded

        model_path = os.path.join(MODELS_DIR, self.model_name)
        if not os.path.exists(model_path):
            raise ModelLoaderError(f"Model file not found: {self.model_name}")

        with open(model_path, "rb") as f:
            self.model = pickle.load(f)
        return self.model

    def load_features(self) -> list:
        """Load the feature columns/vectorizer"""
        if self.feature_columns is not None:
            return self.feature_columns

        feature_path = os.path.join(MODELS_DIR, self.feature_version)
        if not os.path.exists(feature_path):
            raise ModelLoaderError(f"Feature file not found: {self.feature_version}")

        with open(feature_path, "rb") as f:
            self.feature_columns = pickle.load(f)
        return self.feature_columns

    def get_model_metadata(self) -> dict:
        """Return metadata info for endpoints like /metadata"""
        return {
            "active_model": self.model_name,
            "feature_version": self.feature_version,
            "model_type": self.model_type,
            "version": self.version
        }


# =========================
# SINGLETON INSTANCE
# =========================
# This instance can be imported anywhere in the app
model_loader = ModelLoader()


# =========================
# QUICK TEST
# =========================
if __name__ == "__main__":
    ml = ModelLoader()
    print("Metadata:", ml.get_model_metadata())
    model = ml.load_model()
    features = ml.load_features()
    print("Model loaded:", type(model))
    print("Feature columns:", len(features))