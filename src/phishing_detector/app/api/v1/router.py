# 📍 app/api/v1/router.py
from fastapi import APIRouter
from .endpoints import predict, health, metadata

api_v1_router = APIRouter()

# --------------------------
# Route grouping under /v1
# --------------------------
api_v1_router.include_router(predict.router, prefix="", tags=["Predict"])
api_v1_router.include_router(health.router, prefix="", tags=["Health"])
api_v1_router.include_router(metadata.router, prefix="", tags=["Metadata"])