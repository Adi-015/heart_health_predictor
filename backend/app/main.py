from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from loguru import logger

from app.api.routes import predict, health
from app.core.model_loader import load_artifacts

limiter = Limiter(key_func=get_remote_address, default_limits=["20/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading model artifacts...")
    load_artifacts()
    logger.info("Model ready.")
    yield


app = FastAPI(title="Heart Health Predictor API", version="1.0.0", lifespan=lifespan)

# allow_origins=["*"] is fine for a portfolio project — restrict to specific
# Vercel origin(s) in a real production setting
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(health.router, tags=["health"])
app.include_router(predict.router, tags=["predict"])
