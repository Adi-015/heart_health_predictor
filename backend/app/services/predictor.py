import numpy as np
import pandas as pd

from app.core.model_loader import ModelStore
from app.schemas.patient import PatientInput, PredictionResponse, SHAPFactor
from train import FEATURES
from shap_explain import shap_values_for

TOP_N = 5


def predict(patient: PatientInput) -> PredictionResponse:
    row = pd.DataFrame([patient.model_dump()])[FEATURES]
    X = ModelStore.preprocessor.transform(row)

    prob = float(ModelStore.model.predict_proba(X)[0, 1])
    label = "High Risk" if prob >= 0.5 else "Low Risk"

    sv = shap_values_for(ModelStore.explainer, X)
    # sv is (1, n_features) — take the single row
    impacts = sv[0]
    names = ModelStore.feature_names

    # Sort by absolute impact, keep top N
    ranked = sorted(zip(names, impacts), key=lambda x: abs(x[1]), reverse=True)
    top_factors = [
        SHAPFactor(feature=name, impact=round(float(val), 4))
        for name, val in ranked[:TOP_N]
    ]

    return PredictionResponse(
        risk_label=label,
        probability=round(prob, 4),
        top_factors=top_factors,
    )
