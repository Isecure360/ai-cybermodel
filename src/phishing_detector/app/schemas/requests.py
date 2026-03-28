# app/schemas/response.py
from pydantic import BaseModel

class HealthRequests(BaseModel):
    status: str  # e.g., "ok"

class MetadataRequests(BaseModel):
    active_model: str
    feature_version: str
    model_type: str
    version: str