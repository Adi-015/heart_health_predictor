import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
)

# -------------------------------
# Setup
# -------------------------------
os.makedirs("figures", exist_ok=True)
os.makedirs("models", exist_ok=True)

RND = 42
np.random.seed(RND)
random.seed(RND)

# -------------------------------
# Synthetic dataset generator
# -------------------------------
def generate_synthetic_heart_dataset(n_samples=1000, seed=RND):
    np.random.seed(seed)
    ages = np.random.normal(55, 9, size=n_samples).astype(int)
    ages = np.clip(ages, 18, 90)
    genders = np.random.binomial(1, 0.6, size=n_samples)
    rbp = np.random.normal(130, 15, size=n_samples).astype(int)
    rbp = np.clip(rbp, 90, 220)
    chol = np.random.normal(240, 50, size=n_samples).astype(int)
    chol = np.clip(chol, 100, 450)
    max_hr = np.random.normal(150, 22, size=n_samples).astype(int)
    max_hr = np.clip(max_hr, 60, 220)
    fbs = np.random.binomial(1, 0.15, size=n_samples)
    rest_ecg = np.random.choice([0, 1, 2], size=n_samples, p=[0.6, 0.25, 0.15])
    ex_ang = np.random.binomial(1, 0.2, size=n_samples)
    st_dep = np.round(np.random.normal(1.0, 0.8, size=n_samples), 2)
    st_dep = np.clip(st_dep, 0.0, 6.0)
    vessels = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.6, 0.2, 0.15, 0.05])
    chest_pain = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.35, 0.25, 0.25, 0.15])

    risk_score = (
        0.03*(ages-50) + 0.015*(chol-200) + 0.02*(rbp-120) -
        0.02*(max_hr-140) + 0.4*fbs + 0.5*ex_ang +
        0.3*(rest_ecg==1).astype(int) + 0.6*(rest_ecg==2).astype(int) +
        0.4*vessels + 0.25*chest_pain + 0.6*st_dep
    )
    risk_score += np.random.normal(0, 1.2, size=n_samples)
    probs = 1 / (1 + np.exp(-risk_score/3.5))
    target = (probs > 0.5).astype(int)

    df = pd.DataFrame({
        "age": ages,
        "gender": genders,
        "resting_bp": rbp,
        "cholesterol": chol,
        "max_heart_rate": max_hr,
        "fbs_gt_120": fbs,
        "rest_ecg": rest_ecg,
        "exercise_angina": ex_ang,
        "st_depression": st_dep,
        "num_vessels": vessels,
        "chest_pain_type": chest_pain,
        "target": target
    })

    # Add some missing values
    for c in ["cholesterol", "resting_bp", "st_depression"]:
        mask = np.random.rand(n_samples) < 0.02
        df.loc[mask, c] = np.nan

    return df

# -------------------------------
# Generate and save dataset
# -------------------------------
df = generate_synthetic_heart_dataset(1000)
df.to_csv("heart_health.csv", index=False)

print("\n=== Sample of Heart Health Data ===")
print(df.head())

# -------------------------------
# Exploratory Data Analysis
# -------------------------------
plt.figure(figsize=(8,6))
sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("figures/correlation_heatmap.png")
plt.show()

plt.figure(figsize=(6,4))
sns.countplot(x="target", data=df)
plt.title("Target Distribution")
plt.tight_layout()
plt.savefig("figures/target_distribution.png")
plt.show()

plt.figure(figsize=(8,4))
sns.histplot(df["age"].dropna(), bins=20, kde=True)
plt.title("Age Distribution")
plt.tight_layout()
plt.savefig("figures/age_distribution.png")
plt.show()

# -------------------------------
# Preprocessing
# -------------------------------
FEATURES = [
    "age","gender","resting_bp","cholesterol","max_heart_rate",
    "fbs_gt_120","rest_ecg","exercise_angina","st_depression",
    "num_vessels","chest_pain_type"
]
TARGET = "target"

train_df, test_df = train_test_split(df, test_size=0.2, stratify=df[TARGET], random_state=RND)

numeric_features = ["age","resting_bp","cholesterol","max_heart_rate","st_depression"]
cat_features = ["gender","fbs_gt_120","rest_ecg","exercise_angina","num_vessels","chest_pain_type"]

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])
cat_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", cat_transformer, cat_features)
])

# -------------------------------
# Train Logistic Regression
# -------------------------------
X_train, y_train = train_df[FEATURES], train_df[TARGET]
X_test, y_test = test_df[FEATURES], test_df[TARGET]

X_train_p = preprocessor.fit_transform(X_train)
X_test_p = preprocessor.transform(X_test)

lr = LogisticRegression(max_iter=1000, random_state=RND)
lr.fit(X_train_p, y_train)

# -------------------------------
# Evaluation
# -------------------------------
y_pred = lr.predict(X_test_p)
y_prob = lr.predict_proba(X_test_p)[:,1]

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc = roc_auc_score(y_test, y_prob)

print("\n=== Logistic Regression Performance ===")
print(f"Accuracy : {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall   : {rec:.4f}")
print(f"F1-score : {f1:.4f}")
print(f"ROC AUC  : {roc:.4f}")

# -------------------------------
# Confusion Matrix
# -------------------------------
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap="Blues")
plt.title("Confusion Matrix - Logistic Regression")
plt.savefig("figures/confusion_matrix_logistic.png")
plt.show()
