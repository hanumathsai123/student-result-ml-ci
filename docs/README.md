# MLOps Practical Series — Student Result Prediction

This folder contains study guides for the six uploaded practicals. They are organised as Markdown so they can be viewed directly on GitHub.

| Practical | Guide | Main activity |
|---|---|---|
| 5 | [Continuous Delivery](Practical-5-Continuous-Delivery.md) | Flask prediction API tests and release-candidate artifact |
| 6 | [Dockerize Application](Practical-6-Dockerize-Application.md) | Build and run the application container locally |
| 7 | [Automate Docker Build and Test](Practical-7-Automate-Docker-Build-Test.md) | Build/test a container in GitHub Actions |
| 8 | [Publish to GHCR](Practical-8-GHCR-Publish-Image.md) | Publish and pull a tested image from GitHub Container Registry |
| 9 | [GitHub Actions + GHCR](Practical-9-GitHub-Actions-GHCR.md) | Automate Docker build, tests and image publication |
| 10 | [Deploy GHCR Image to Render](Practical-10-Deploy-GHCR-Image-to-Render.md) | Deploy the registry image as a Render web service |

## Compatibility note

The repository originally contains the model-training CI workflow for the Student Result Prediction project. The guides preserve that project as the foundation. Practical 5–9 examples are adapted to its currently inspected Flask app/model bundle conventions. Before deploying, ensure each workflow's port and endpoint match the exact application built into your Docker image.

The original Practical-9 and Practical-10 handouts describe a FastAPI variant using port 8000 and `/health`/`/docs`; the current model CI repository did not contain `app.py` or `Dockerfile` at the time these guides were added. Review the compatibility notes in each guide before running deployment steps.

Practical 5–10 guides are documentation; adding them does not mean the corresponding code or cloud deployment has already been executed or verified.
