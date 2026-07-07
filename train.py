import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend, safe for scripted runs
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay,
)
import joblib

from data.load_data import load_heart_data
from preprocess import build_preprocessing_pipeline

RND = 42

NUMERIC = ["age", "trestbps", "chol", "thalach", "oldpeak"]
CATEGORICAL = ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"]
FEATURES = NUMERIC + CATEGORICAL
TARGET = "target"


def evaluate(model, X, y, name):
    y_pred = model.predict(X)
    y_prob = model.predict_proba(X)[:, 1]
    return {
        "model": name,
        "accuracy":  round(accuracy_score(y, y_pred), 4),
        "precision": round(precision_score(y, y_pred), 4),
        "recall":    round(recall_score(y, y_pred), 4),
        "f1":        round(f1_score(y, y_pred), 4),
        "roc_auc":   round(roc_auc_score(y, y_prob), 4),
    }


def save_confusion_matrix(model, X, y, name, out_dir="figures"):
    os.makedirs(out_dir, exist_ok=True)
    cm = confusion_matrix(y, model.predict(X))
    disp = ConfusionMatrixDisplay(cm)
    disp.plot(cmap="Blues")
    plt.title(f"Confusion Matrix — {name}")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, f"cm_{name.lower().replace(' ', '_')}.png"))
    plt.close()


if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)

    df = load_heart_data()
    train_df, test_df = train_test_split(df, test_size=0.2, stratify=df[TARGET], random_state=RND)

    preprocessor = build_preprocessing_pipeline(NUMERIC, CATEGORICAL)
    X_train = preprocessor.fit_transform(train_df[FEATURES])
    X_test  = preprocessor.transform(test_df[FEATURES])
    y_train, y_test = train_df[TARGET], test_df[TARGET]

    lr = LogisticRegression(max_iter=1000, random_state=RND)
    lr.fit(X_train, y_train)

    metrics = evaluate(lr, X_test, y_test, "Logistic Regression")

    print("\n=== Logistic Regression on UCI Cleveland ===")
    for k, v in metrics.items():
        print(f"  {k:<12}: {v}")

    save_confusion_matrix(lr, X_test, y_test, "Logistic Regression")
    joblib.dump(lr, "models/logistic_regression.pkl")

    pd.DataFrame([metrics]).to_csv("results/logistic_regression.csv", index=False)
    print("\nResults saved to results/logistic_regression.csv")
