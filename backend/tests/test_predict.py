import sys
import pytest
from fastapi.testclient import TestClient

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.main import app

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

VALID_PATIENT = {
    "age": 54, "sex": 1, "cp": 0, "trestbps": 140,
    "chol": 239, "fbs": 0, "restecg": 1, "thalach": 160,
    "exang": 0, "oldpeak": 1.2, "slope": 1, "ca": 0, "thal": 2,
}


def test_predict_valid_input(client):
    resp = client.post("/predict", json=VALID_PATIENT)
    assert resp.status_code == 200
    data = resp.json()
    assert data["risk_label"] in ("High Risk", "Low Risk")
    assert 0.0 <= data["probability"] <= 1.0
    assert isinstance(data["top_factors"], list)
    assert len(data["top_factors"]) > 0
    assert "feature" in data["top_factors"][0]
    assert "impact" in data["top_factors"][0]


def test_predict_probability_regression(client):
    # Canonical value produced by the saved model + saved preprocessor during Day 2 evaluation.
    # If this drifts it means the loaded artifacts changed or the preprocessor is being re-fit.
    resp = client.post("/predict", json=VALID_PATIENT)
    assert resp.status_code == 200
    prob = resp.json()["probability"]
    assert abs(prob - 0.7208) < 0.001, f"Probability drifted: expected ~0.7208, got {prob}"


def test_predict_missing_field(client):
    bad = {k: v for k, v in VALID_PATIENT.items() if k != "thal"}
    resp = client.post("/predict", json=bad)
    assert resp.status_code == 422


def test_predict_out_of_range_age(client):
    bad = {**VALID_PATIENT, "age": 200}
    resp = client.post("/predict", json=bad)
    assert resp.status_code == 422


def test_predict_wrong_type(client):
    bad = {**VALID_PATIENT, "age": "fifty-four"}
    resp = client.post("/predict", json=bad)
    assert resp.status_code == 422


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_model_info(client):
    resp = client.get("/model-info")
    assert resp.status_code == 200
    data = resp.json()
    assert "model_type" in data
    assert "metrics" in data
