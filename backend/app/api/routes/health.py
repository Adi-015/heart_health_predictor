from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/model-info")
def model_info():
    return {"status": "stub — implemented in commit 5"}
