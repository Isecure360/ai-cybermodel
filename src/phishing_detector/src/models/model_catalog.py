# src/models/model_catalog.py

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

def get_models():
    return {
        "random_forest": RandomForestClassifier(),
        "logistic_regression": LogisticRegression(max_iter=1000),
        "gradient_boosting": GradientBoostingClassifier(),
    }