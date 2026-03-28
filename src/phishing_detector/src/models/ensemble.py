# 📍 src/models/ensemble.py

from sklearn.ensemble import VotingClassifier


def build_ensemble(top_results):
    estimators = []

    for entry in top_results:
        name = entry["name"]
        model = entry["model"]
        estimators.append((name, model))

    ensemble = VotingClassifier(
        estimators=estimators,
        voting="soft"  # uses probabilities
    )

    return ensemble

def train_ensemble(ensemble, X_train, y_train):
    ensemble.fit(X_train, y_train)
    return ensemble

