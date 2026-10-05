import json
import os
import unittest

import joblib
import numpy as np
import pandas as pd


class TestMLPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset_path = "student_results.csv"
        cls.model_path = "student_result_model.pkl"
        cls.metrics_path = "metrics.json"

    def test_dataset_created(self):
        self.assertTrue(os.path.exists(self.dataset_path))
        df = pd.read_csv(self.dataset_path)
        self.assertEqual(len(df), 300)

    def test_model_created(self):
        self.assertTrue(os.path.exists(self.model_path))

    def test_metrics_created(self):
        self.assertTrue(os.path.exists(self.metrics_path))

    def test_accuracy_valid(self):
        with open(self.metrics_path, encoding="utf-8") as f:
            metrics = json.load(f)
        accuracy = metrics["accuracy"]
        self.assertGreaterEqual(accuracy, 0.0)
        self.assertLessEqual(accuracy, 1.0)

    def test_model_prediction_valid(self):
        bundle = joblib.load(self.model_path)
        X = pd.DataFrame(
            [[90, 90, 90, 90]],
            columns=[
                "attendance",
                "internal_marks",
                "assignment_marks",
                "previous_score",
            ],
        )
        scaled = bundle["scaler"].transform(X)
        prediction = bundle["model"].predict(scaled)[0]
        self.assertIn(int(prediction), [0, 1])

    def test_high_performance_prediction(self):
        bundle = joblib.load(self.model_path)
        X = pd.DataFrame(
            [[95, 95, 95, 95]],
            columns=[
                "attendance",
                "internal_marks",
                "assignment_marks",
                "previous_score",
            ],
        )
        scaled = bundle["scaler"].transform(X)
        prediction = bundle["model"].predict(scaled)[0]
        self.assertEqual(int(prediction), 1)

    def test_low_performance_prediction(self):
        bundle = joblib.load(self.model_path)
        X = pd.DataFrame(
            [[50, 40, 40, 40]],
            columns=[
                "attendance",
                "internal_marks",
                "assignment_marks",
                "previous_score",
            ],
        )
        scaled = bundle["scaler"].transform(X)
        prediction = bundle["model"].predict(scaled)[0]
        self.assertEqual(int(prediction), 0)


if __name__ == "__main__":
    unittest.main()
