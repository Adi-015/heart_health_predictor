FROM python:3.10-slim

WORKDIR /app

# ML deps first — they're heavier and change less often than app code
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/requirements.txt ./backend_requirements.txt
RUN pip install --no-cache-dir -r backend_requirements.txt

# Copy everything needed: ML modules, models/, data/, backend/
COPY preprocess.py train.py shap_explain.py ./
COPY data/ ./data/
COPY models/ ./models/
COPY backend/ ./backend/

# PYTHONPATH=/app lets backend code import ML modules (preprocess, train, etc.) from repo root
ENV PYTHONPATH=/app

EXPOSE 8000

# Run from backend/ so 'from app.api.routes import ...' resolves correctly
WORKDIR /app/backend
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
