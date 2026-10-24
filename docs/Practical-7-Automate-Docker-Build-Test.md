# Practical-7: Automate Docker Build and Test Using GitHub Actions

Continuation of Practical-6. This practical automates Docker build, container startup, health verification, and prediction API testing in GitHub Actions. It does not publish an image to a registry.

## Objective
Validate the final container runtime on a GitHub-hosted runner after ML training, quality gate, and tests pass.

## Prerequisites
- Working `train_model.py`, `quality_gate.py`, and automated tests.
- Flask application `app.py`, Dockerfile, `.dockerignore`, and requirements.
- Application binds to `0.0.0.0:5000`.

## Workflow steps
Add the following steps to `.github/workflows/ml-ci.yml` after model/application tests. They assume the workflow already trained `student_result_model.pkl` before Docker build.

```yaml
      - name: Build Docker image
        run: docker build -t student-result-ml:${{ github.sha }} .

      - name: Start Docker container
        run: |
          docker run -d \
            --name student-result-ml-container \
            -p 5000:5000 \
            student-result-ml:${{ github.sha }}

      - name: Wait for application to become ready
        run: |
          for i in {1..15}; do
            if curl --fail --silent http://localhost:5000/; then
              echo "Application is ready."
              exit 0
            fi
            echo "Waiting for application... attempt $i"
            sleep 2
          done
          echo "Application did not become ready."
          docker logs student-result-ml-container
          exit 1

      - name: Test prediction endpoint
        run: |
          response=$(curl --fail --silent --show-error \
            -X POST -H "Content-Type: application/json" \
            -d '{"attendance":95,"internal_marks":95,"assignment_marks":95,"previous_score":95}' \
            http://localhost:5000/predict)
          echo "Prediction response: $response"
          echo "$response" | grep -q '"prediction":"PASS"'

      - name: Show Docker container logs
        if: always()
        run: docker logs student-result-ml-container || true

      - name: Stop and remove Docker container
        if: always()
        run: docker rm -f student-result-ml-container || true
```

## Verify
Push the workflow changes and inspect the Actions run:
1. Existing training and quality-gate steps pass.
2. ML/application tests pass.
3. Docker image builds.
4. Container starts and responds on port 5000.
5. Prediction endpoint returns PASS for the high-performing sample.
6. Logs are captured and container cleanup runs even on failure.

**Endpoint note:** the provided Practical-5 app uses `/` as its status endpoint, not `/health`. If you adopt `/health`, add it to the app and use it consistently in the workflow.
