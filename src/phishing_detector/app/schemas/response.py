# app/schemas/response.py
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str  # e.g., "ok"

class MetadataResponse(BaseModel):
    active_model: str
    feature_version: str
    model_type: str
    version: str