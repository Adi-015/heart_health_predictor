import sys
import json
import joblib
from pathlib import Path

from app.core.config import REPO_ROOT, MODEL_PATH, METADATA_PATH

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from train import NUMERIC, CATEGORICAL
from shap_explain import build_explainer

PREPROCESSOR_PATH = REPO_ROOT / "models" / "preprocessor.pkl"


class ModelStore:
    model = None
    preprocessor = None
    explainer = None
    feature_names: list = []
    metadata: dict = {}


def load_artifacts():
    ModelStore.model = joblib.load(MODEL_PATH)
    ModelStore.preprocessor = joblib.load(PREPROCESSOR_PATH)

    with open(METADATA_PATH) as f:
        ModelStore.metadata = json.load(f)

    ohe = ModelStore.preprocessor.named_transformers_["cat"].named_steps["onehot"]
    ModelStore.feature_names = NUMERIC + list(ohe.get_feature_names_out(CATEGORICAL))

    # Build explainer against training-distribution data using the fitted preprocessor.
    # We need a small background matrix — load just enough for TreeExplainer initialisation.
    from data.load_data import load_heart_data
    from sklearn.model_selection import train_test_split
    from train import FEATURES
    df = load_heart_data()
    train_df, _ = train_test_split(df, test_size=0.2, stratify=df["target"], random_state=42)
    X_background = ModelStore.preprocessor.transform(train_df[FEATURES])
    ModelStore.explainer = build_explainer(ModelStore.model, X_background)
