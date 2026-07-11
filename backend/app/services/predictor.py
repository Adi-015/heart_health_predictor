import numpy as np
import pandas as pd
from loguru import logger

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
    impacts = sv[0]
    names = ModelStore.feature_names

    ranked = sorted(zip(names, impacts), key=lambda x: abs(x[1]), reverse=True)
    top_factors = [
        SHAPFactor(feature=name, impact=round(float(val), 4))
        for name, val in ranked[:TOP_N]
    ]

    # Log summary — no raw field values to stay privacy-conscious
    logger.info(
        "prediction | age={} sex={} result={} prob={:.4f} top_feature={}",
        patient.age, patient.sex, label, prob,
        top_factors[0].feature if top_factors else "n/a",
    )

    return PredictionResponse(
        risk_label=label,
        probability=round(prob, 4),
        top_factors=top_factors,
    )
