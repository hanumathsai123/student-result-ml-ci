# Practical-10: Deploy the Tested Docker Image from GHCR to Render

Continuation of Practical-9. Deploy the existing tested image; do not retrain the model or build a separate image for this practical.

## Objective
Create a public Render Web Service from the Student Result Prediction image published to GitHub Container Registry (GHCR), then verify the live HTTP endpoints.

## 1. Confirm the image from Practical-9
Open GitHub → Packages and verify that `student-result-prediction` exists with a recent `latest` tag. Expected image format:
```text
ghcr.io/hanumathsai123/student-result-prediction:latest
```

If the package is private, configure a Render registry credential using a GitHub Personal Access Token (classic) with only `read:packages` permission. Never paste the token into this repository or screenshots.

## 2. Create an image-backed Render Web Service
1. Sign in to the Render Dashboard.
2. Choose **New → Web Service**.
3. Select **Existing Image**.
4. Enter the GHCR image reference.
5. Configure the service name, region and plan available to your account.
6. Make the service's configured port and health path match the image.

## 3. Check port and endpoints carefully
The earlier Flask application in this repository uses port **5000**, root endpoint `/`, and prediction endpoint `/predict`. The Practical-9/10 handouts describe a separate FastAPI example using port **8000** and endpoints `/health` and `/docs`. Use the port and paths built into the actual GHCR image—do not configure the Flask image as though it were the FastAPI image.

For the Flask image, check:
- `/` — service status JSON
- `/predict` — POST JSON with attendance, internal_marks, assignment_marks, previous_score

Example request:
```bash
curl --fail --show-error -X POST "https://YOUR-SERVICE.onrender.com/predict" \
  -H 'Content-Type: application/json' \
  -d '{"attendance":95,"internal_marks":95,"assignment_marks":95,"previous_score":95}'
```
Replace `YOUR-SERVICE` with the actual Render service hostname.

## 4. Deploy and verify
1. Create the service and wait for deployment to finish.
2. Review deployment events and runtime logs if it fails.
3. Open the public HTTPS URL and test the root endpoint.
4. Submit the prediction request and record the returned JSON.
5. Record the public service URL and image tag/commit for reproducibility.

## Important
An image-backed service does not necessarily redeploy automatically when the GHCR tag changes. Redeploy the image from the Render dashboard after Practical-9 publishes an updated version. Do not publish credentials in the practical record.
