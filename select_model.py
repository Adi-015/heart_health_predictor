import os
import json
import datetime
import joblib
import pandas as pd

from tune import load_data_splits, tune_random_forest, tune_xgboost, tune_logistic_regression, save_md_table
from train import evaluate, save_confusion_matrix

os.makedirs("results", exist_ok=True)
os.makedirs("models", exist_ok=True)


def run_all_tuned():
    X_train, X_test, y_train, y_test, preprocessor = load_data_splits()

    tuners = [
        ("Logistic Regression (tuned)", tune_logistic_regression),
        ("Random Forest (tuned)",       tune_random_forest),
        ("XGBoost (tuned)",             tune_xgboost),
    ]

    results = []
    best_params_map = {}

    for name, tuner in tuners:
        print(f"Tuning {name}...")
        model, params = tuner(X_train, y_train)
        metrics = evaluate(model, X_test, y_test, name)
        results.append((name, model, params, metrics))
        best_params_map[name] = params
        print(f"  recall={metrics['recall']}  f1={metrics['f1']}  roc_auc={metrics['roc_auc']}")

    return results, X_test, y_test, preprocessor


def pick_winner(results):
    # Primary: recall. Tiebreaker: roc_auc.
    return max(results, key=lambda r: (r[3]["recall"], r[3]["roc_auc"]))


if __name__ == "__main__":
    results, X_test, y_test, preprocessor = run_all_tuned()

    rows = [r[3] for r in results]
    save_md_table(rows, "results/tuned_model_comparison.md", "Tuned Model Comparison — UCI Cleveland")

    winner_name, winner_model, winner_params, winner_metrics = pick_winner(results)
    print(f"\nWinner: {winner_name}")
    print(f"  recall={winner_metrics['recall']}  roc_auc={winner_metrics['roc_auc']}")

    save_confusion_matrix(winner_model, X_test, y_test, winner_name)
    joblib.dump(winner_model, "models/model.pkl")
    joblib.dump(preprocessor, "models/preprocessor.pkl")

    metadata = {
        "model_type":   winner_name,
        "hyperparams":  {k: (float(v) if hasattr(v, "item") else v) for k, v in winner_params.items()},
        "metrics":      winner_metrics,
        "dataset_size": 303,
        "date":         datetime.date.today().isoformat(),
        "reason":       "Highest recall on test set (primary metric for medical screening); ROC AUC used as tiebreaker.",
    }
    with open("models/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print("\nSaved models/model.pkl, models/preprocessor.pkl, and models/metadata.json")
    print("\n=== Tuned Model Comparison ===")
    print(pd.DataFrame(rows).set_index("model").to_string())
