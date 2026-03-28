'''
✅ Notes
Uses Pydantic for validation: any invalid URL is rejected automatically.
Returns prediction + probability.
Errors inside the predictor are caught and returned as 500 Internal Server Error.
Plugged into your existing router:
'''


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.services.predictor import predict_url

router = APIRouter()

# =========================
# REQUEST / RESPONSE SCHEMAS
# =========================
class PredictRequest(BaseModel):
    url: HttpUrl  # ensures valid URL

class PredictResponse(BaseModel):
    url: str
    prediction: int  # 0 = legit, 1 = phishing
    probability: float


# =========================
# /predict ENDPOINT
# =========================
@router.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    try:
        result = predict_url(request.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))