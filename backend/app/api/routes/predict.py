from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.schemas.patient import PatientInput, PredictionResponse
from app.services import predictor

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/predict", response_model=PredictionResponse)
@limiter.limit("20/minute")
def predict_route(request: Request, patient: PatientInput):
    return predictor.predict(patient)
