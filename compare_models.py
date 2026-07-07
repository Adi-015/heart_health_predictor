import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from data.load_data import load_heart_data
from preprocess import build_preprocessing_pipeline
from train import evaluate, save_confusion_matrix, NUMERIC, CATEGORICAL, FEATURES, TARGET

RND = 42


def build_models():
    return [
        ("Logistic Regression", LogisticRegression(max_iter=1000, random_state=RND)),
        ("Random Forest",       RandomForestClassifier(n_estimators=100, random_state=RND)),
        ("XGBoost",             XGBClassifier(n_estimators=100, eval_metric="logloss", random_state=RND)),
    ]


if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)

    df = load_heart_data()
    train_df, test_df = train_test_split(df, test_size=0.2, stratify=df[TARGET], random_state=RND)

    preprocessor = build_preprocessing_pipeline(NUMERIC, CATEGORICAL)
    X_train = preprocessor.fit_transform(train_df[FEATURES])
    X_test  = preprocessor.transform(test_df[FEATURES])
    y_train, y_test = train_df[TARGET], test_df[TARGET]

    results = []
    for name, model in build_models():
        model.fit(X_train, y_train)
        metrics = evaluate(model, X_test, y_test, name)
        results.append(metrics)
        save_confusion_matrix(model, X_test, y_test, name)
        print(f"  {name}: accuracy={metrics['accuracy']}  f1={metrics['f1']}  roc_auc={metrics['roc_auc']}")

    comparison = pd.DataFrame(results).set_index("model")

    comparison.to_csv("results/model_comparison.csv")

    # Markdown table
    md_lines = ["# Model Comparison — UCI Cleveland Heart Disease\n"]
    md_lines.append("| Model | Accuracy | Precision | Recall | F1 | ROC AUC |")
    md_lines.append("|---|---|---|---|---|---|")
    for model_name, row in comparison.iterrows():
        md_lines.append(
            f"| {model_name} | {row['accuracy']} | {row['precision']} | {row['recall']} | {row['f1']} | {row['roc_auc']} |"
        )
    with open("results/model_comparison.md", "w") as f:
        f.write("\n".join(md_lines))

    print("\n=== Model Comparison ===")
    print(comparison.to_string())
    print("\nSaved to results/model_comparison.csv and results/model_comparison.md")
