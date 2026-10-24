FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY train_model.py .
COPY quality_gate.py .
COPY test_ml_pipeline.py .
COPY test_app.py .

EXPOSE 5000

CMD ["sh", "-c", "python train_model.py && python app.py"]
