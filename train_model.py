import json
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix


RANDOM_STATE = 42
N_STUDENTS = 300


def main():
    np.random.seed(RANDOM_STATE)

    df = pd.DataFrame({
        "attendance": np.random.randint(50, 101, N_STUDENTS),
        "internal_marks": np.random.randint(40, 101, N_STUDENTS),
        "assignment_marks": np.random.randint(40, 101, N_STUDENTS),
        "previous_score": np.random.randint(40, 101, N_STUDENTS),
    })

    df["weighted_score"] = (
        0.25 * df["attendance"]
        + 0.35 * df["internal_marks"]
        + 0.20 * df["assignment_marks"]
        + 0.20 * df["previous_score"]
    )

    df["result"] = (df["weighted_score"] >= 60).astype(int)
    df.to_csv("student_results.csv", index=False)

    X = df[
        ["attendance", "internal_marks", "assignment_marks", "previous_score"]
    ]
    y = df["result"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    model_bundle = {
        "scaler": scaler,
        "model": model,
        "features": [
            "attendance",
            "internal_marks",
            "assignment_marks",
            "previous_score",
        ],
    }

    joblib.dump(model_bundle, "student_result_model.pkl")

    metrics = {
        "accuracy": float(accuracy),
        "confusion_matrix": cm.tolist(),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
    }

    with open("metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"Students: {len(df)}")
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Accuracy: {accuracy:.4f}")
    print("Confusion Matrix:")
    print(cm)
    print("Model saved: student_result_model.pkl")
    print("Metrics saved: metrics.json")


if __name__ == "__main__":
    main()
