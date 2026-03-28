# 📍 src/models/experiment_tracker.py

import os
import json
import datetime

EXPERIMENTS_DIR = "experiments"


def log_experiment(results):
    os.makedirs(EXPERIMENTS_DIR, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    experiment_file = os.path.join(EXPERIMENTS_DIR, f"experiment_{timestamp}.json")

    serializable_results = []

    for r in results:
        serializable_results.append({
            "model": r["name"],
            "metrics": r["metrics"],
            "confusion_matrix": r["confusion_matrix"]
        })

    with open(experiment_file, "w") as f:
        json.dump(serializable_results, f, indent=4)

    print(f"🧪 Experiment logged → {experiment_file}")