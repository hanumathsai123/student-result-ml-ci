from pathlib import Path
import os

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MODEL_PATH = Path("student_result_model.pkl")
FEATURES = ["attendance", "internal_marks", "assignment_marks", "previous_score"]

app = FastAPI(
    title="Student Result Prediction API",
    description="Predict a student's result from attendance and assessment marks.",
    version="1.0.0",
)


class StudentInput(BaseModel):
    attendance: float = Field(..., ge=0, le=100, description="Attendance percentage")
    internal_marks: float = Field(..., ge=0, le=100, description="Internal marks")
    assignment_marks: float = Field(..., ge=0, le=100, description="Assignment marks")
    previous_score: float = Field(..., ge=0, le=100, description="Previous exam score")


def load_model():
    if not MODEL_PATH.exists():
        raise HTTPException(status_code=503, detail="Model file is not available yet.")
    return joblib.load(MODEL_PATH)


@app.get("/", tags=["default"])
def root():
    return {"status": "ok", "service": "student-result-prediction", "docs": "/docs"}


@app.get("/health", tags=["default"])
def health():
    return {"status": "ok", "service": "student-result-prediction"}


@app.post("/predict", tags=["default"])
def predict(student: StudentInput):
    bundle = load_model()
    sample = pd.DataFrame([[getattr(student, feature) for feature in FEATURES]], columns=FEATURES)
    scaled = bundle["scaler"].transform(sample)
    prediction_code = int(bundle["model"].predict(scaled)[0])
    return {
        "prediction": "PASS" if prediction_code == 1 else "FAIL",
        "prediction_code": prediction_code,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
