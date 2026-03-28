'''
1️⃣ config.py — Environment & Settings Loader

Purpose: Central place to read .env or YAML config so your API and model paths aren’t hard-coded.
'''

# app/core/config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # API
    API_TITLE: str = "Phishing Detection System"
    API_VERSION: str = "1.0"
    
    # Model paths
    MODELS_DIR: str = os.getenv("MODELS_DIR", "models")
    REGISTRY_FILE: str = os.getenv("REGISTRY_FILE", "registry.json")
    
    # Optional: logging level
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"

settings = Settings()