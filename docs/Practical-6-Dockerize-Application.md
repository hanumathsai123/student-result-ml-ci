# Practical-6: Dockerize the ML Prediction Application

Continuation of Practical-5. This practical builds and tests the Docker image manually on the local system. Automated Docker build/test belongs to Practical-7.

## Objective
Package the Flask prediction application, trained model, Python runtime, and dependencies into a Docker image, run it as a container, and verify the API.

## Prerequisites
- Successful release candidate artifact `student-result-ml-release` from Practical-5.
- Docker Desktop/Engine installed and running.
- Extracted release directory containing `app.py`, `student_result_model.pkl`, `metrics.json`, and `requirements.txt`.

## 1. Verify Docker
```bash
docker --version
docker info
docker run --rm hello-world
```

## 2. Create `Dockerfile`
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY student_result_model.pkl .
COPY metrics.json .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 3. Create `.dockerignore`
```text
__pycache__/
*.pyc
.git/
.github/
test_*.py
student_results.csv
release_candidate/
```

## 4. Build and run
Run these commands from the directory containing the Dockerfile and application files:
```bash
docker build -t student-result-ml:local .
docker run -d --name student-result-ml-container -p 5000:5000 student-result-ml:local
docker ps
curl http://localhost:5000/
```

Test prediction:
```bash
curl --fail --show-error -X POST http://localhost:5000/predict \
  -H 'Content-Type: application/json' \
  -d '{"attendance":95,"internal_marks":95,"assignment_marks":95,"previous_score":95}'
```

Expected prediction is PASS for the high-performing sample.

## 5. Inspect and clean up
```bash
docker logs student-result-ml-container
docker stop student-result-ml-container
docker rm student-result-ml-container
```

## Important
The supplied Practical-5 sample `app.py` uses the root endpoint `/` as its health/status endpoint and port 5000. Do not use `/health` or port 8000 unless you separately change the application and its callers consistently.
