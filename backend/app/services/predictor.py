import numpy as np
import pandas as pd

from app.core.model_loader import ModelStore
from app.schemas.patient import PatientInput, PredictionResponse, SHAPFactor
from train import FEATURES


def predict(patient: PatientInput) -> PredictionResponse:
    row = pd.DataFrame([patient.model_dump()])[FEATURES]
    X = ModelStore.preprocessor.transform(row)

    prob = float(ModelStore.model.predict_proba(X)[0, 1])
    label = "High Risk" if prob >= 0.5 else "Low Risk"

    return PredictionResponse(
        risk_label=label,
        probability=round(prob, 4),
        top_factors=[],
    )
