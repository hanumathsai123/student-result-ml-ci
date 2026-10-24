# Practical-8: Publish the Tested Docker Image to GitHub Container Registry (GHCR)

Continuation of Practical-7. Reuse the already-tested local image; do not retrain the model or rebuild the image merely for registry publication.

## Objective
Authenticate Docker to GHCR, tag the tested image, push versioned and latest tags, pull the published image, run it, and verify the API.

## 1. Check the tested image
```bash
docker images
```
Use the exact image name/tag that passed Practical-7. The examples below assume `student-result-ml:local`; replace it if your local tag differs.

## 2. Create a GitHub token
In GitHub Settings → Developer settings → Personal access tokens → Tokens (classic), create a token with `write:packages` and `read:packages` for this publishing/pull lab. Never commit the token or include it in reports or screenshots.

Log in interactively so the token is not saved in shell history:
```bash
read -s GHCR_TOKEN
echo "$GHCR_TOKEN" | docker login ghcr.io -u hanumathsai123 --password-stdin
unset GHCR_TOKEN
```

## 3. Tag the existing tested image
```bash
docker tag student-result-ml:local ghcr.io/hanumathsai123/student-result-prediction:v1
docker tag student-result-ml:local ghcr.io/hanumathsai123/student-result-prediction:latest
docker images
```

## 4. Push to GHCR
```bash
docker push ghcr.io/hanumathsai123/student-result-prediction:v1
docker push ghcr.io/hanumathsai123/student-result-prediction:latest
```

## 5. Pull and run the published image
```bash
docker pull ghcr.io/hanumathsai123/student-result-prediction:v1
docker run -d --name student-result-from-ghcr -p 5000:5000 ghcr.io/hanumathsai123/student-result-prediction:v1
curl http://localhost:5000/
curl --fail --show-error -X POST http://localhost:5000/predict \
  -H 'Content-Type: application/json' \
  -d '{"attendance":95,"internal_marks":95,"assignment_marks":95,"previous_score":95}'
docker logs student-result-from-ghcr
docker rm -f student-result-from-ghcr
```

## Verify
Open the repository owner's GitHub profile → Packages → `student-result-prediction`. Confirm the tags exist, and that the pulled container responds as expected.

**Important:** If your existing Docker image uses port 8000 or a different API, continue using the exact verified port and endpoint from your earlier practical instead of mixing configurations.
