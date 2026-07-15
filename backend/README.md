# Backend — Heart Health Predictor API

FastAPI service that serves predictions from a tuned Random Forest model with SHAP explanations.

## Local dev

```bash
# From repo root
cd backend
pip install -r requirements.txt
pip install -r ../requirements.txt   # ML deps
uvicorn app.main:app --reload --port 8001
```

Or with Docker Compose from repo root:
```bash
docker compose up backend
```

## Deploying to Render

1. Push the branch to GitHub (Render watches your repo).
2. Go to [render.com](https://render.com) → **New** → **Web Service**.
3. Connect your GitHub repo and select it.
4. Set these options:
   - **Environment**: Docker
   - **Dockerfile path**: `backend/Dockerfile`
   - **Docker build context**: `.` (repo root — important, not `backend/`)
5. Add environment variable: `PYTHONPATH` = `/app`
6. Click **Deploy**. Render will run `docker build` and start the container.
7. The `/health` endpoint is configured as the health check in `render.yaml`.

> **Note**: `model.pkl` and `preprocessor.pkl` are currently committed to the repo (they're in `.gitignore` locally but need to be present in the Docker image). If you want to keep them out of git, use Render's [persistent disk](https://render.com/docs/disks) or a storage bucket and add a download step to the Dockerfile.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/model-info` | Model type, metrics, hyperparams |
| POST | `/predict` | Takes `PatientInput`, returns `PredictionResponse` with SHAP factors |

See `app/schemas/patient.py` for the full request/response schema.
