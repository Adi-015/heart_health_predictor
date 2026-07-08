from tune import load_data_splits, tune_logistic_regression, save_md_table
from train import evaluate, save_confusion_matrix
import joblib, json

if __name__ == "__main__":
    X_train, X_test, y_train, y_test, _ = load_data_splits()

    print("Tuning Logistic Regression (scoring=recall, cv=5)...")
    model, params = tune_logistic_regression(X_train, y_train)

    print(f"Best params: {params}")
    metrics = evaluate(model, X_test, y_test, "Logistic Regression (tuned)")
    print(f"  recall={metrics['recall']}  f1={metrics['f1']}  roc_auc={metrics['roc_auc']}")

    save_confusion_matrix(model, X_test, y_test, "Logistic Regression Tuned")
    save_md_table([metrics], "results/tuned_lr.md", "Tuned Logistic Regression")

    joblib.dump(model, "models/tuned_lr.pkl")
    with open("models/tuned_lr_params.json", "w") as f:
        json.dump(params, f, indent=2)
    print("Saved models/tuned_lr.pkl and models/tuned_lr_params.json")
