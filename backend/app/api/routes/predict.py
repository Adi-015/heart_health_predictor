from fastapi import APIRouter
from app.schemas.patient import PatientInput, PredictionResponse
from app.services import predictor

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
def predict(patient: PatientInput):
    return predictor.predict(patient)
