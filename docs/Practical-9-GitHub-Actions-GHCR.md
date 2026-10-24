# Practical-9: Automate Docker Image Build, Test, and Publish to GHCR Using GitHub Actions

Continuation of Practical-8. The workflow builds a Docker image, runs a temporary test container, checks its API, and only then publishes latest and commit-specific tags to GHCR.

## Before starting
Confirm the Dockerfile and running application in this repository agree on the port and health path. The existing repository Practical-5/6 example uses Flask on port 5000 and `/` as the status endpoint. The original Practical-9 handout uses FastAPI port 8000 and `/health`; do not mix the two contracts. This workflow adapts the handout's release pattern to the Flask application currently documented in this repository.

## Add `.github/workflows/docker-publish.yml`
```yaml
name: Build, Test and Publish Student Result Prediction

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  packages: write

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: student-result-prediction

jobs:
  build-test-publish:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7

      - name: Set up Python
        uses: actions/setup-python@v7
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Train model
        run: python train_model.py

      - name: Build Docker image
        run: docker build -t "$IMAGE_NAME:ci" .

      - name: Start test container
        run: docker run -d --name student-result-ci -p 5000:5000 "$IMAGE_NAME:ci"

      - name: Test API status endpoint
        run: |
          for attempt in {1..20}; do
            if curl --fail --silent http://localhost:5000/; then
              echo "Status check passed."
              exit 0
            fi
            echo "Waiting for API..."
            sleep 3
          done
          docker logs student-result-ci
          exit 1

      - name: Test prediction endpoint
        run: |
          response=$(curl --fail --silent --show-error             -X POST -H "Content-Type: application/json"             -d '{"attendance":95,"internal_marks":95,"assignment_marks":95,"previous_score":95}'             http://localhost:5000/predict)
          echo "$response"
          echo "$response" | grep -q '"prediction":"PASS"'

      - name: Remove test container
        if: always()
        run: docker rm -f student-result-ci || true

      - name: Prepare lowercase image name
        run: |
          IMAGE_ID="ghcr.io/${{ github.repository_owner }}/${IMAGE_NAME}"
          IMAGE_ID=$(echo "$IMAGE_ID" | tr '[:upper:]' '[:lower:]')
          echo "IMAGE_ID=$IMAGE_ID" >> "$GITHUB_ENV"

      - name: Log in to GHCR
        run: |
          echo "${{ secrets.GITHUB_TOKEN }}" |             docker login "$REGISTRY" -u "${{ github.actor }}" --password-stdin

      - name: Tag tested image
        run: |
          docker tag "$IMAGE_NAME:ci" "$IMAGE_ID:latest"
          docker tag "$IMAGE_NAME:ci" "$IMAGE_ID:sha-${{ github.sha }}"

      - name: Push tested image to GHCR
        run: |
          docker push "$IMAGE_ID:latest"
          docker push "$IMAGE_ID:sha-${{ github.sha }}"
```

## Verify
1. Commit and push to `main` or run manually through Actions.
2. Confirm Docker build and status/prediction checks pass.
3. Confirm GHCR login and both pushes pass.
4. Open GitHub Packages and verify `latest` and `sha-<commit>` tags.

If `requirements.txt` does not yet include Flask, update it as in Practical-5. Never store a personal access token in the repository; this workflow uses the automatically generated `GITHUB_TOKEN`.
