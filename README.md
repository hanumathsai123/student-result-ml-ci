# Student Result Prediction — MLOps CI/CD

This repository trains a student pass/fail classifier and validates a Flask prediction API. GitHub Actions runs the ML quality gate and automated tests, builds a Docker image, validates its endpoints, and publishes the tested image to GitHub Container Registry (GHCR).

## ML model
The training pipeline creates a reproducible synthetic dataset of 300 students using attendance, internal marks, assignment marks, and previous score. It writes `student_results.csv`, `student_result_model.pkl`, and `metrics.json`.

## API
- `GET /` — service status
- `GET /health` — health check
- `POST /predict` — JSON body with `attendance`, `internal_marks`, `assignment_marks`, and `previous_score`

Example:
```bash
curl --fail --show-error -X POST http://localhost:5000/predict \
  -H 'Content-Type: application/json' \
  -d '{"attendance":95,"internal_marks":95,"assignment_marks":95,"previous_score":95}'
```

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python train_model.py
python quality_gate.py
python -m unittest discover -v
python app.py
```

## Docker
```bash
docker build -t student-result-prediction:local .
docker run --rm -p 5000:5000 student-result-prediction:local
```

## Practical progression
- Practical 2–4: model training, quality gate, tests and artifacts in `.github/workflows/ml-ci.yml`.
- Practical 5: API tests and release candidate packaging.
- Practical 6–7: Docker build and runtime validation.
- Practical 8–9: publish the tested image to GHCR.
- Practical 10: deploy the GHCR image to Render. Match the deployed image's port (5000 for this Flask app) and endpoint (`/health`).

Implementation guides based on the uploaded practicals are in `docs/`. A guide in the repository does not mean its steps have already been run successfully.
