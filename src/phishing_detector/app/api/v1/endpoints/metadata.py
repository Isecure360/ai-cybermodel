# 📍 app/api/v1/endpoints/metadata.py

from fastapi import APIRouter
from app.services.model_loader import model_loader

router = APIRouter()

@router.get("/metadata")
def get_model_metadata():
    """
    Returns the current active model and feature info.
    """
    return model_loader.get_model_metadata()