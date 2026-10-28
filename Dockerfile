FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY api.py .
COPY train_model.py .
COPY quality_gate.py .

EXPOSE 5000

CMD ["sh", "-c", "python train_model.py && uvicorn api:app --host 0.0.0.0 --port ${PORT:-5000}"]
