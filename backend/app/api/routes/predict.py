from fastapi import APIRouter

router = APIRouter()


@router.post("/predict")
def predict():
    return {"status": "stub — implemented in commit 3"}
