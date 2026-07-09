import sys
import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

from app.core.config import REPO_ROOT, MODEL_PATH, METADATA_PATH

# ML modules live at repo root — add to path before importing
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from preprocess import build_preprocessing_pipeline
from train import NUMERIC, CATEGORICAL, FEATURES
from data.load_data import load_heart_data
from sklearn.model_selection import train_test_split
from shap_explain import build_explainer, shap_values_for


class ModelStore:
    model = None
    preprocessor = None
    explainer = None
    feature_names: list = []
    metadata: dict = {}


def load_artifacts():
    ModelStore.model = joblib.load(MODEL_PATH)

    with open(METADATA_PATH) as f:
        ModelStore.metadata = json.load(f)

    df = load_heart_data()
    train_df, _ = train_test_split(df, test_size=0.2, stratify=df["target"], random_state=42)
    preprocessor = build_preprocessing_pipeline(NUMERIC, CATEGORICAL)
    preprocessor.fit(train_df[FEATURES])
    ModelStore.preprocessor = preprocessor

    ohe = preprocessor.named_transformers_["cat"].named_steps["onehot"]
    ModelStore.feature_names = NUMERIC + list(ohe.get_feature_names_out(CATEGORICAL))

    X_train = preprocessor.transform(train_df[FEATURES])
    ModelStore.explainer = build_explainer(ModelStore.model, X_train)
