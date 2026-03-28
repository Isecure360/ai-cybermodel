# utils/dummy_model.py

import random

def predict_url(url: str):
    url = url.lower()

    if any(x in url for x in ["login", "verify", "bank", "secure"]):
        return "phishing", round(random.uniform(0.75, 0.95), 2)

    return "benign", round(random.uniform(0.75, 0.95), 2)