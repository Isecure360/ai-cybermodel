# 📍 src/models/performance.py

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

def evaluate_models(models, X_train, X_test, y_train, y_test):
    results = []

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        metrics = {
            "accuracy": accuracy_score(y_test, preds),
            "precision": precision_score(y_test, preds, zero_division=0),
            "recall": recall_score(y_test, preds, zero_division=0),
            "f1_score": f1_score(y_test, preds, zero_division=0),
        }

        cm = confusion_matrix(y_test, preds).tolist()
        report = classification_report(y_test, preds, output_dict=True)

        results.append({
            "name": name,
            "model": model,
            "metrics": metrics,
            "confusion_matrix": cm,
            "classification_report": report
        })

    return sorted(results, key=lambda x: x["metrics"]["f1_score"], reverse=True)
import datetime
import pickle
import os

def save_top_models(results, feature_columns):
    os.makedirs("models", exist_ok=True)

    top_models = results[:2]

    for i, entry in enumerate(top_models):
        model = entry["model"]
        name = entry["name"]

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        model_filename = f"{name}_v{i+1}_{timestamp}.pkl"
        feature_filename = f"features_v{i+1}_{timestamp}.pkl"

        with open(f"models/{model_filename}", "wb") as f:
            pickle.dump(model, f)

        with open(f"models/{feature_filename}", "wb") as f:
            pickle.dump(feature_columns, f)

        print(f"✅ Saved: {model_filename}")