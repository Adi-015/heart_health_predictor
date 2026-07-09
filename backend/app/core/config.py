import os
from pathlib import Path

# Repo root is two levels up from backend/app/core/
REPO_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = REPO_ROOT / "models" / "model.pkl"
METADATA_PATH = REPO_ROOT / "models" / "metadata.json"
DATA_PATH = REPO_ROOT / "data"
