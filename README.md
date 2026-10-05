# Student Result ML Model with GitHub Actions CI

This repository implements Practical-2: a machine-learning CI pipeline using GitHub Actions.

## What the pipeline does

1. Generates a reproducible student-result dataset with 300 students.
2. Creates four input features:
   - attendance
   - internal_marks
   - assignment_marks
   - previous_score
3. Calculates a weighted score and labels the result as pass (1) or fail (0).
4. Splits the data into 80% training and 20% testing sets.
5. Scales features using StandardScaler.
6. Trains a Logistic Regression classifier.
7. Evaluates accuracy and a confusion matrix.
8. Saves the trained model and metrics.
9. Runs automated unit tests.

## GitHub Actions

The workflow in `.github/workflows/ml-ci.yml` runs on pushes to `main`, pull requests to `main`, and manual workflow dispatch.

Generated files such as `student_results.csv`, `student_result_model.pkl`, and `metrics.json` are created during CI and are not committed to the repository.

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python train_model.py
python -m unittest discover -v
```
