import os
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)
MODEL_PATH = Path("student_result_model.pkl")
FEATURES = ["attendance", "internal_marks", "assignment_marks", "previous_score"]


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("student_result_model.pkl was not found. Run train_model.py first.")
    return joblib.load(MODEL_PATH)


@app.get("/")
def health_check():
    return jsonify({"status": "ok", "service": "student-result-prediction"})


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "student-result-prediction"})


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "JSON request body is required"}), 400
    missing = [feature for feature in FEATURES if feature not in data]
    if missing:
        return jsonify({"error": "Missing required fields", "missing_fields": missing}), 400
    try:
        sample = pd.DataFrame([{feature: float(data[feature]) for feature in FEATURES}])
    except (TypeError, ValueError):
        return jsonify({"error": "Feature values must be numeric"}), 400
    bundle = load_model()
    scaled = bundle["scaler"].transform(sample)
    prediction_code = int(bundle["model"].predict(scaled)[0])
    return jsonify({"prediction": "PASS" if prediction_code == 1 else "FAIL",
                    "prediction_code": prediction_code})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
