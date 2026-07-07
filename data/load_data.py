import pandas as pd
import urllib.request
import os

# Cleveland dataset from UCI via a stable mirror on GitHub
_CSV_URL = (
    "https://raw.githubusercontent.com/sharmaroshan/"
    "Heart-UCI-Dataset/master/heart.csv"
)
_LOCAL_PATH = os.path.join(os.path.dirname(__file__), "heart_cleveland.csv")


def load_heart_data() -> pd.DataFrame:
    """
    Returns the UCI Cleveland Heart Disease dataset as a DataFrame.

    Downloads the CSV on first call and caches it locally at
    data/heart_cleveland.csv. Subsequent calls read from the cache.

    Target column: 'target' — 0 = no disease, 1 = disease.
    The raw UCI file uses values 0–4; anything > 0 is collapsed to 1 here
    so it stays a binary classification problem.
    """
    if not os.path.exists(_LOCAL_PATH):
        urllib.request.urlretrieve(_CSV_URL, _LOCAL_PATH)

    df = pd.read_csv(_LOCAL_PATH)

    # Normalise column names used in the wild (some mirrors differ)
    df.columns = [c.strip().lower() for c in df.columns]

    # Collapse multi-class target to binary if needed
    if df["target"].max() > 1:
        df["target"] = (df["target"] > 0).astype(int)

    return df


if __name__ == "__main__":
    df = load_heart_data()
    print(f"Loaded {len(df)} rows, {df.shape[1]} columns")
    print(df.head())
    print("\nTarget distribution:")
    print(df["target"].value_counts())
