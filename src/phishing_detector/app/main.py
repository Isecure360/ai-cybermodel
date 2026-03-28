# 📍 app/main.py
from fastapi import FastAPI
from app.api.v1.router import api_v1_router  # ✅ correct import
from app.core.logging import setup_logging

# Initialize logging
setup_logging()

# Initialize FastAPI
app = FastAPI(
    title="Phishing Detection System",
    version="1.0",
    description="API for detecting phishing URLs using the promoted URL-only model"
)

# Include versioned routes
app.include_router(api_v1_router, prefix="/api/v1")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Phishing Detection API is live! Go to /api/v1/health to check status."}