from fastapi import FastAPI
from app.api.routes import predict, health

app = FastAPI(title="Heart Health Predictor API", version="1.0.0")

app.include_router(health.router, tags=["health"])
app.include_router(predict.router, tags=["predict"])
