import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import joblib

from data.load_data import load_heart_data
from preprocess import build_preprocessing_pipeline
from train import evaluate, save_confusion_matrix, NUMERIC, CATEGORICAL, FEATURES, TARGET

RND = 42
os.makedirs("results", exist_ok=True)
os.makedirs("models", exist_ok=True)


def load_data_splits():
    df = load_heart_data()
    train_df, test_df = train_test_split(df, test_size=0.2, stratify=df[TARGET], random_state=RND)
    preprocessor = build_preprocessing_pipeline(NUMERIC, CATEGORICAL)
    X_train = preprocessor.fit_transform(train_df[FEATURES])
    X_test  = preprocessor.transform(test_df[FEATURES])
    return X_train, X_test, train_df[TARGET], test_df[TARGET], preprocessor


def tune_random_forest(X_train, y_train):
    param_dist = {
        "n_estimators":      [100, 200, 300, 500],
        "max_depth":         [None, 5, 10, 15, 20],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf":  [1, 2, 4],
        "class_weight":      [None, "balanced"],
    }
    search = RandomizedSearchCV(
        RandomForestClassifier(random_state=RND),
        param_dist,
        n_iter=40,
        scoring="recall",
        cv=5,
        random_state=RND,
        n_jobs=-1,
    )
    search.fit(X_train, y_train)
    return search.best_estimator_, search.best_params_


def tune_xgboost(X_train, y_train):
    # scale_pos_weight helps when optimising recall on imbalanced data
    neg, pos = (y_train == 0).sum(), (y_train == 1).sum()
    param_dist = {
        "n_estimators":    [100, 200, 300],
        "max_depth":       [3, 4, 5, 6, 8],
        "learning_rate":   [0.01, 0.05, 0.1, 0.2],
        "subsample":       [0.7, 0.8, 0.9, 1.0],
        "scale_pos_weight": [1, neg / pos, 2 * neg / pos],
    }
    search = RandomizedSearchCV(
        XGBClassifier(eval_metric="logloss", random_state=RND),
        param_dist,
        n_iter=40,
        scoring="recall",
        cv=5,
        random_state=RND,
        n_jobs=-1,
    )
    search.fit(X_train, y_train)
    return search.best_estimator_, search.best_params_


def tune_logistic_regression(X_train, y_train):
    # 'balanced' class_weight tends to meaningfully boost recall on small medical datasets
    param_grid = {
        "C":            [0.001, 0.01, 0.1, 0.5, 1, 5, 10, 50, 100],
        "penalty":      ["l1", "l2"],
        "class_weight": [None, "balanced"],
        "solver":       ["liblinear"],  # supports both l1 and l2
    }
    search = RandomizedSearchCV(
        LogisticRegression(max_iter=1000, random_state=RND),
        param_grid,
        n_iter=30,
        scoring="recall",
        cv=5,
        random_state=RND,
        n_jobs=-1,
    )
    search.fit(X_train, y_train)
    return search.best_estimator_, search.best_params_


def save_md_table(rows, path, title):
    lines = [f"# {title}\n"]
    lines.append("| Model | Accuracy | Precision | Recall | F1 | ROC AUC |")
    lines.append("|---|---|---|---|---|---|")
    for r in rows:
        lines.append(
            f"| {r['model']} | {r['accuracy']} | {r['precision']} | {r['recall']} | {r['f1']} | {r['roc_auc']} |"
        )
    with open(path, "w") as f:
        f.write("\n".join(lines))
