# MLOps Practical Series — Student Result Prediction

This repository now includes **runnable implementation files** for the practical series. The guides are supporting notes; the actual code lives at the project root and the GitHub Actions workflow.

| Practical | Implemented repository files | Main activity |
|---|---|---|
| 5 | `app.py`, `test_app.py`, `requirements.txt`, `.github/workflows/ml-ci.yml` | Flask API, tests, release artifact |
| 6 | `Dockerfile`, `.dockerignore` | Containerize application |
| 7 | `.github/workflows/ml-ci.yml` | Build and test image in CI |
| 8 | Existing published-image flow / manual GHCR commands in [guide](Practical-8-GHCR-Publish-Image.md) | Pull and push image tags |
| 9 | `.github/workflows/ml-ci.yml` | Automatically publish tested image to GHCR on pushes to main |
| 10 | Deployment instructions in [guide](Practical-10-Deploy-GHCR-Image-to-Render.md) | Deploy the GHCR image using Render |

## Repository links

- [Application](../app.py)
- [API tests](../test_app.py)
- [Dockerfile](../Dockerfile)
- [GitHub Actions workflow](../.github/workflows/ml-ci.yml)
- [Project README](../README.md)

## Port and endpoint convention

This implementation follows the Flask app in Practical 5: container port **5000**, `GET /`, `GET /health`, and `POST /predict`. The supplied Practical 9–10 handouts mention a different FastAPI convention on port 8000; use the concrete Flask endpoints and port for this repository.

The GitHub Actions workflow is now configured to test the Flask API in a Docker container and publish the image to GHCR on pushes to `main`. Check the Actions run to verify the result. Render service creation is a manual dashboard step and has not been performed automatically.
