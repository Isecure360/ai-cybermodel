import os
import shutil
import json

# ===== CONFIG =====
SOURCE_DIR = "models/model_trials/url_only"
TARGET_DIR = "models"

MODEL_NAME = "model_v1.pkl"
FEATURE_NAME = "features_v1.pkl"

PROMOTED_MODEL_NAME = "phishing_model_v1.pkl"
PROMOTED_FEATURE_NAME = "features_v1.pkl"

REGISTRY_PATH = os.path.join(TARGET_DIR, "registry.json")


# ===== ENSURE TARGET DIR EXISTS =====
os.makedirs(TARGET_DIR, exist_ok=True)


# ===== PATHS =====
source_model_path = os.path.join(SOURCE_DIR, MODEL_NAME)
source_feature_path = os.path.join(SOURCE_DIR, FEATURE_NAME)

target_model_path = os.path.join(TARGET_DIR, PROMOTED_MODEL_NAME)
target_feature_path = os.path.join(TARGET_DIR, PROMOTED_FEATURE_NAME)


# ===== VALIDATION =====
if not os.path.exists(source_model_path):
    raise FileNotFoundError(f"❌ Model not found: {source_model_path}")

if not os.path.exists(source_feature_path):
    raise FileNotFoundError(f"❌ Features not found: {source_feature_path}")


# ===== COPY FILES =====
shutil.copy2(source_model_path, target_model_path)
shutil.copy2(source_feature_path, target_feature_path)

print("✅ Model and features copied successfully")


# ===== CREATE / UPDATE REGISTRY =====
registry_data = {
    "active_model": PROMOTED_MODEL_NAME,
    "feature_version": PROMOTED_FEATURE_NAME,
    "model_type": "url_only",
    "version": "v1"
}

with open(REGISTRY_PATH, "w") as f:
    json.dump(registry_data, f, indent=4)

print("✅ registry.json updated")


# ===== DONE =====
print("🚀 Model promotion complete!")