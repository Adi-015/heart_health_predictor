from fastapi import APIRouter
from app.core.model_loader import ModelStore

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/model-info")
def model_info():
    m = ModelStore.metadata
    return {
        "model_type": m.get("model_type"),
        "date":        m.get("date"),
        "dataset_size": m.get("dataset_size"),
        "reason":       m.get("reason"),
        "metrics":      m.get("metrics"),
        "hyperparams":  m.get("hyperparams"),
    }
