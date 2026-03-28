# 📍 src/pipelines/training_pipeline.py

from src.models.ensemble import build_ensemble, train_ensemble

from src.data.ingest import load_all_datasets
from src.features.build_features import build_features
from src.models.model_catalog import get_models
from src.models.split import split_data
from src.models.performance import evaluate_models
from src.models.save_results import save_top_models_and_results, save_promoted_model
from src.models.registry import promote_best_model
from src.models.experiment_tracker import log_experiment


def run_training_pipeline():
    print("🚀 Starting training pipeline...")

    dfs = load_all_datasets()
    df = build_features(dfs)

    X = df.drop(columns=["label"])
    y = df["label"]

    X_train, X_test, y_train, y_test = split_data(X, y)

    models = get_models()

    results = evaluate_models(models, X_train, X_test, y_train, y_test)

    print("\n📊 Performance Summary:")
    for r in results:
        print(f"{r['name']} → {r['metrics']}")

    # 🧪 Log experiment
    log_experiment(results)

    # 💾 Save top 2 models (for record keeping)
    save_top_models_and_results(results, X.columns.tolist())

    # -------------------------------
    # 🤖 ENSEMBLE SECTION
    # -------------------------------
    top_2 = results[:2]

    ensemble = build_ensemble(top_2)
    ensemble = train_ensemble(ensemble, X_train, y_train)

    from sklearn.metrics import f1_score

    ensemble_preds = ensemble.predict(X_test)
    ensemble_f1 = f1_score(y_test, ensemble_preds)

    print(f"\n🤖 Ensemble F1 Score: {ensemble_f1}")

    # -------------------------------
    # 🏆 MODEL SELECTION LOGIC
    # -------------------------------
    best_model_entry = results[0]
    best_model = best_model_entry["model"]
    best_name = best_model_entry["name"]
    best_metrics = best_model_entry["metrics"]

    best_f1 = best_metrics["f1_score"]

    if ensemble_f1 > best_f1:
        print("🔥 Ensemble beats best model → promoting ensemble")

        promoted_model = ensemble
        promoted_name = "ensemble_model"
        promoted_metrics = {
            "f1_score": ensemble_f1,
            "type": "ensemble"
        }

    else:
        print("📌 Best single model remains king")

        promoted_model = best_model
        promoted_name = best_name
        promoted_metrics = best_metrics

    # -------------------------------
    # 💾 SAVE + PROMOTE FINAL WINNER
    # -------------------------------
    folder = save_promoted_model(
        promoted_model,
        promoted_name,
        promoted_metrics,
        X.columns.tolist()
    )

    promote_best_model(folder, promoted_name, promoted_metrics)

    print("✅ System updated with best model!")