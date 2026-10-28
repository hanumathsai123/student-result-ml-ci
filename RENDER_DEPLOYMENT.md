# Render deployment — Practical 10

This project publishes its tested Docker image to GitHub Container Registry (GHCR) using GitHub Actions. Render can deploy the image as a public web service.

## 1. Publish the latest image
1. Open the repository's Actions tab.
2. Run the "Student Result ML CI/CD" workflow manually, or push a change to `main`.
3. Wait for every job to finish successfully, including the Docker test and GHCR publish steps.

The image name configured in the workflow is:
`ghcr.io/hanumathsai123/student-result-prediction:latest`

If the GHCR package is private, make it public in GitHub Packages or configure Render with a registry credential that has read access.

## 2. Create the Render service
1. Sign in to Render and choose **New + → Web Service**.
2. Choose **Existing Image** (Docker image) as the source.
3. Enter `ghcr.io/hanumathsai123/student-result-prediction:latest`.
4. Set the service port to `5000` if Render asks for a port. The container also honors Render's `PORT` environment variable.
5. Deploy the service and wait for the status to become **Live**.

## 3. Verify the public service
Replace `YOUR-RENDER-SERVICE.onrender.com` with the hostname Render gives you.

- Root: `https://YOUR-RENDER-SERVICE.onrender.com/`
- Health: `https://YOUR-RENDER-SERVICE.onrender.com/health`
- Swagger UI: `https://YOUR-RENDER-SERVICE.onrender.com/docs`
- Prediction: use `POST https://YOUR-RENDER-SERVICE.onrender.com/predict` with JSON:
```json
{
  "attendance": 95,
  "internal_marks": 95,
  "assignment_marks": 95,
  "previous_score": 95
}
```

A successful response contains a `prediction` value such as `PASS` or `FAIL`.

## Status
The repository configuration is prepared for the Render deployment. The actual public URL is only available after the image is published and the service is created in the Render account.
