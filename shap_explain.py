import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shap
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from preprocess import build_preprocessing_pipeline
from train import NUMERIC, CATEGORICAL, FEATURES, TARGET

os.makedirs("results", exist_ok=True)


def get_feature_names(preprocessor):
    num_names = NUMERIC
    ohe = preprocessor.named_transformers_["cat"].named_steps["onehot"]
    cat_names = list(ohe.get_feature_names_out(CATEGORICAL))
    return num_names + cat_names


def build_explainer(model, X_background):
    """
    Returns a SHAP explainer appropriate for the model type.
    X_background only used for LinearExplainer / KernelExplainer fallback.
    XGBClassifier must be trained with base_score=0.5 (explicit float) to
    avoid a shap 0.49 / XGBoost 3.x bracketed base_score parsing bug.
    """
    if isinstance(model, (XGBClassifier, RandomForestClassifier)):
        return shap.TreeExplainer(model)
    if isinstance(model, LogisticRegression):
        return shap.LinearExplainer(model, X_background)
    return shap.KernelExplainer(model.predict_proba, shap.sample(X_background, 50))


def shap_values_for(explainer, X):
    vals = explainer.shap_values(X)
    # RF returns [class0_vals, class1_vals]; tree/linear return a single array
    if isinstance(vals, list):
        return vals[1]
    return vals


def generate_summary_plot(model, X_test, feature_names, out_path="results/shap_summary.png"):
    explainer = build_explainer(model, X_test)
    sv = shap_values_for(explainer, X_test)

    shap.summary_plot(sv, X_test, feature_names=feature_names, show=False)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_path}")
    return sv, explainer


def generate_waterfall_plot(explainer, X_test, sv, idx=0,
                            feature_names=None,
                            out_path="results/shap_example_waterfall.png"):
    """
    Waterfall plot for a single prediction at row `idx`.
    Returns the shap.Explanation so callers can reuse it (e.g. per-request in the backend).
    """
    expected = explainer.expected_value
    if isinstance(expected, (list, np.ndarray)):
        expected = float(expected[1])

    row_data = X_test[idx] if not hasattr(X_test[idx], "toarray") else X_test[idx].toarray().flatten()

    explanation = shap.Explanation(
        values=sv[idx],
        base_values=expected,
        data=row_data,
        feature_names=feature_names,
    )
    shap.plots.waterfall(explanation, show=False)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_path}")
    return explanation


if __name__ == "__main__":
    from sklearn.model_selection import train_test_split
    from data.load_data import load_heart_data

    df = load_heart_data()
    train_df, test_df = train_test_split(df, test_size=0.2, stratify=df[TARGET], random_state=42)

    preprocessor = build_preprocessing_pipeline(NUMERIC, CATEGORICAL)
    preprocessor.fit_transform(train_df[FEATURES])
    X_test = preprocessor.transform(test_df[FEATURES])

    model = joblib.load("models/model.pkl")
    feature_names = get_feature_names(preprocessor)

    sv, explainer = generate_summary_plot(model, X_test, feature_names)
    generate_waterfall_plot(explainer, X_test, sv, idx=0, feature_names=feature_names)
