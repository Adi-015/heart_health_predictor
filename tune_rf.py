from tune import load_data_splits, tune_random_forest, save_md_table
from train import evaluate, save_confusion_matrix

if __name__ == "__main__":
    X_train, X_test, y_train, y_test, _ = load_data_splits()

    print("Tuning Random Forest (scoring=recall, cv=5)...")
    model, params = tune_random_forest(X_train, y_train)

    print(f"Best params: {params}")
    metrics = evaluate(model, X_test, y_test, "Random Forest (tuned)")
    print(f"  recall={metrics['recall']}  f1={metrics['f1']}  roc_auc={metrics['roc_auc']}")

    save_confusion_matrix(model, X_test, y_test, "Random Forest Tuned")
    save_md_table([metrics], "results/tuned_rf.md", "Tuned Random Forest")

    import joblib, json
    joblib.dump(model, "models/tuned_rf.pkl")
    with open("models/tuned_rf_params.json", "w") as f:
        json.dump(params, f, indent=2)
    print("Saved models/tuned_rf.pkl and models/tuned_rf_params.json")
