# 📍 src/models/registry.py

import os
import json

REGISTRY_PATH = "models/registry.json"


def promote_best_model(model_folder, model_name, metrics):
    registry = {
        "active_model_path": f"{model_folder}/model.pkl",
        "features_path": f"{model_folder}/features.pkl",
        "model_name": model_name,
        "promoted_at": model_folder,
        "metrics": metrics
    }

    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=4)

    print(f"🚀 Promoted model → {model_name}")