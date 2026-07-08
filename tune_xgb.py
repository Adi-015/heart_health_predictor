from tune import load_data_splits, tune_xgboost, save_md_table
from train import evaluate, save_confusion_matrix
import joblib, json

if __name__ == "__main__":
    X_train, X_test, y_train, y_test, _ = load_data_splits()

    print("Tuning XGBoost (scoring=recall, cv=5)...")
    model, params = tune_xgboost(X_train, y_train)

    print(f"Best params: {params}")
    metrics = evaluate(model, X_test, y_test, "XGBoost (tuned)")
    print(f"  recall={metrics['recall']}  f1={metrics['f1']}  roc_auc={metrics['roc_auc']}")

    save_confusion_matrix(model, X_test, y_test, "XGBoost Tuned")
    save_md_table([metrics], "results/tuned_xgb.md", "Tuned XGBoost")

    joblib.dump(model, "models/tuned_xgb.pkl")
    with open("models/tuned_xgb_params.json", "w") as f:
        json.dump(params, f, indent=2, default=float)
    print("Saved models/tuned_xgb.pkl and models/tuned_xgb_params.json")
