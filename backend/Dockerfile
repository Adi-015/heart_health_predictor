FROM python:3.10-slim

WORKDIR /app

# Install ML dependencies first (heavier, changes less often)
COPY requirements.txt ./backend_requirements.txt
RUN pip install --no-cache-dir -r backend_requirements.txt

# Copy the full repo so ML modules (preprocess.py, train.py, shap_explain.py, models/) are reachable
COPY .. /app

# Install ML project requirements
RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
