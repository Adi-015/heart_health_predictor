from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import predict, health
from app.core.model_loader import load_artifacts


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_artifacts()
    yield


app = FastAPI(title="Heart Health Predictor API", version="1.0.0", lifespan=lifespan)

app.include_router(health.router, tags=["health"])
app.include_router(predict.router, tags=["predict"])
