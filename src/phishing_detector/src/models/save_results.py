# 📍 src/models/save_results.py

import os
import json
import datetime
import pickle

BASE_DIR = "models"


def save_top_models_and_results(results, feature_columns):
    os.makedirs(BASE_DIR, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    top_models = results[:2]

    promoted_model_folder = None
    promoted_model_name = None
    promoted_metrics = None

    for i, entry in enumerate(top_models):
        name = entry["name"]
        model = entry["model"]
        metrics = entry["metrics"]

        folder_name = f"{name}_results_{timestamp}"
        folder_path = os.path.join(BASE_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Save model
        with open(f"{folder_path}/model.pkl", "wb") as f:
            pickle.dump(model, f)

        # Save features
        with open(f"{folder_path}/features.pkl", "wb") as f:
            pickle.dump(feature_columns, f)

        # Save metrics
        with open(f"{folder_path}/metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)

        # Save confusion matrix + report
        with open(f"{folder_path}/confusion_matrix.json", "w") as f:
            json.dump(entry["confusion_matrix"], f, indent=4)

        with open(f"{folder_path}/classification_report.json", "w") as f:
            json.dump(entry["classification_report"], f, indent=4)

        print(f"🏆 Saved → {folder_name}")

        # First model = best
        if i == 0:
            promoted_model_folder = folder_path
            promoted_model_name = name
            promoted_metrics = metrics

    return promoted_model_folder, promoted_model_name, promoted_metrics

def save_promoted_model(model, name, metrics, feature_columns):
    import datetime

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    folder_name = f"{name}_promoted_{timestamp}"
    folder_path = os.path.join(BASE_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Save model
    with open(f"{folder_path}/model.pkl", "wb") as f:
        pickle.dump(model, f)

    # Save features
    with open(f"{folder_path}/features.pkl", "wb") as f:
        pickle.dump(feature_columns, f)

    # Save metrics
    with open(f"{folder_path}/metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    print(f"🚀 Promoted model saved → {folder_name}")

    return folder_path