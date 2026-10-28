from pathlib import Path
import logging
import os
import time
import uuid

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from prometheus_client import Counter, Gauge, Histogram, CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel, Field

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("student_result_api")

MODEL_PATH = Path("student_result_model.pkl")
FEATURES = ["attendance", "internal_marks", "assignment_marks", "previous_score"]

HTTP_REQUESTS = Counter(
    "student_api_http_requests_total",
    "Total HTTP requests handled by the API",
    ["method", "endpoint", "status_code"],
)
HTTP_REQUEST_DURATION = Histogram(
    "student_api_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)
PREDICTIONS = Counter(
    "student_api_predictions_total",
    "Prediction outcomes returned by the model",
    ["result"],
)
MODEL_AVAILABLE = Gauge(
    "student_api_model_available",
    "Whether the model file is available (1=yes, 0=no)",
)

app = FastAPI(
    title="Student Result Prediction API",
    description="Predict a student's result from attendance and assessment marks.",
    version="1.2.0",
)


class StudentInput(BaseModel):
    attendance: float = Field(..., ge=0, le=100, description="Attendance percentage")
    internal_marks: float = Field(..., ge=0, le=100, description="Internal marks")
    assignment_marks: float = Field(..., ge=0, le=100, description="Assignment marks")
    previous_score: float = Field(..., ge=0, le=100, description="Previous exam score")


@app.middleware("http")
async def observe_requests(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    started = time.perf_counter()
    status_code = 500
    endpoint = request.url.path
    try:
        response = await call_next(request)
        status_code = response.status_code
        response.headers["X-Request-ID"] = request_id
        return response
    except Exception:
        logger.exception(
            "request_failed request_id=%s method=%s path=%s",
            request_id, request.method, endpoint,
        )
        raise
    finally:
        duration = time.perf_counter() - started
        HTTP_REQUESTS.labels(request.method, endpoint, str(status_code)).inc()
        HTTP_REQUEST_DURATION.labels(request.method, endpoint).observe(duration)
        duration_ms = round(duration * 1000, 2)
        level = logging.WARNING if status_code >= 400 else logging.INFO
        logger.log(
            level,
            "request_complete request_id=%s method=%s path=%s status_code=%s duration_ms=%s",
            request_id, request.method, endpoint, status_code, duration_ms,
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_types = [error.get("type", "unknown") for error in exc.errors()]
    logger.warning(
        "request_validation_failed method=%s path=%s error_types=%s",
        request.method, request.url.path, error_types,
    )
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


def load_model():
    MODEL_AVAILABLE.set(1 if MODEL_PATH.exists() else 0)
    if not MODEL_PATH.exists():
        logger.error("model_unavailable path=%s", MODEL_PATH)
        raise HTTPException(status_code=503, detail="Model file is not available yet.")
    try:
        return joblib.load(MODEL_PATH)
    except Exception as exc:
        logger.exception("model_load_failed error_type=%s", type(exc).__name__)
        raise HTTPException(status_code=503, detail="Model could not be loaded.") from exc


@app.get("/", tags=["default"])
def root():
    return {"status": "ok", "service": "student-result-prediction", "docs": "/docs", "metrics": "/metrics"}


@app.get("/health", tags=["default"])
def health():
    available = MODEL_PATH.exists()
    MODEL_AVAILABLE.set(1 if available else 0)
    if not available:
        raise HTTPException(status_code=503, detail="Model file is not available.")
    return {"status": "ok", "service": "student-result-prediction", "model_available": True}


@app.get("/metrics", include_in_schema=False)
def metrics():
    MODEL_AVAILABLE.set(1 if MODEL_PATH.exists() else 0)
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict", tags=["default"])
def predict(student: StudentInput):
    bundle = load_model()
    sample = pd.DataFrame([[getattr(student, feature) for feature in FEATURES]], columns=FEATURES)
    scaled = bundle["scaler"].transform(sample)
    prediction_code = int(bundle["model"].predict(scaled)[0])
    result = "PASS" if prediction_code == 1 else "FAIL"
    PREDICTIONS.labels(result).inc()
    logger.info("prediction_completed prediction=%s", result)
    return {"prediction": result, "prediction_code": prediction_code}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
