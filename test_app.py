import unittest

from app import app


class TestPredictionApplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The model is generated in the preceding CI training step.
        from train_model import main
        main()

    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_health_alias(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

    def test_high_performance_prediction(self):
        response = self.client.post("/predict", json={
            "attendance": 95, "internal_marks": 95,
            "assignment_marks": 95, "previous_score": 95
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["prediction"], "PASS")

    def test_low_performance_prediction(self):
        response = self.client.post("/predict", json={
            "attendance": 50, "internal_marks": 40,
            "assignment_marks": 40, "previous_score": 40
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["prediction"], "FAIL")

    def test_missing_field_validation(self):
        response = self.client.post("/predict", json={"attendance": 90, "internal_marks": 85})
        self.assertEqual(response.status_code, 400)
        self.assertIn("missing_fields", response.get_json())

    def test_non_numeric_validation(self):
        response = self.client.post("/predict", json={
            "attendance": "high", "internal_marks": 85,
            "assignment_marks": 80, "previous_score": 75
        })
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
