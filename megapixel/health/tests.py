from django.test import TestCase

from .services import engine


class RiskEngineTests(TestCase):
    def test_metrics_are_normalized(self):
        metrics = engine.compute_metrics(
            {
                "height_cm": 175,
                "weight_kg": 78,
                "activity_level": "medium",
                "sleep_hours": 6.5,
                "junk_food_frequency": "medium",
                "sugar_intake": "medium",
                "water_liters": 2.2,
                "stress_level": 6,
                "work_hours": 9,
                "family_history": True,
                "smoking": False,
            }
        )
        self.assertGreaterEqual(metrics.overall_health, 0)
        self.assertLessEqual(metrics.overall_health, 100)
        self.assertGreaterEqual(metrics.heart_risk, 0)
        self.assertLessEqual(metrics.heart_risk, 100)

    def test_silent_risk_detection(self):
        msg = engine.detect_silent_risk([8, 9, 7, 8, 8])
        self.assertIsNotNone(msg)
