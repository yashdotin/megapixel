from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

import numpy as np
from sklearn.ensemble import RandomForestRegressor


CATEGORY_SCORE = {
    "low": 30,
    "medium": 60,
    "high": 90,
    "poor": 35,
    "average": 65,
    "good": 90,
}


@dataclass
class HealthMetrics:
    bmi: float
    activity_score: float
    sleep_score: float
    diet_score: float
    stress_score: float
    energy_score: float
    lifestyle_score: float
    diabetes_risk: float
    heart_risk: float
    bp_risk: float
    burnout_risk: float
    sleep_disorder_risk: float
    fatigue_risk: float
    diet_risk: float
    overall_health: float
    explainability: dict


class RiskEngine:
    def __init__(self) -> None:
        self.model = RandomForestRegressor(n_estimators=80, random_state=42)
        self._fit_bootstrap_model()

    def _fit_bootstrap_model(self) -> None:
        rng = np.random.default_rng(42)
        n = 450
        bmi = rng.uniform(16, 38, n)
        activity = rng.uniform(15, 95, n)
        sleep = rng.uniform(20, 95, n)
        diet = rng.uniform(15, 95, n)
        stress = rng.uniform(10, 95, n)
        family = rng.integers(0, 2, n)
        smoking = rng.integers(0, 2, n)

        X = np.column_stack([bmi, activity, sleep, diet, stress, family, smoking])
        y = (
            0.25 * np.clip((bmi - 18) * 3.4, 0, 100)
            + 0.20 * (100 - activity)
            + 0.15 * (100 - sleep)
            + 0.15 * (100 - diet)
            + 0.20 * stress
            + 5 * family
            + 5 * smoking
        )
        y = np.clip(y, 5, 98)
        self.model.fit(X, y)

    def compute_metrics(self, payload: dict) -> HealthMetrics:
        height_m = payload["height_cm"] / 100
        bmi = payload["weight_kg"] / (height_m**2)

        activity_score = CATEGORY_SCORE.get(payload.get("activity_level", "medium"), 60)
        sleep_score = self._sleep_score(payload.get("sleep_hours", 7))

        junk_component = 100 - CATEGORY_SCORE.get(payload.get("junk_food_frequency", "medium"), 60)
        sugar_component = 100 - CATEGORY_SCORE.get(payload.get("sugar_intake", "medium"), 60)
        water_component = min(100, max(20, payload.get("water_liters", 2) * 30))
        diet_score = (junk_component + sugar_component + water_component) / 3

        stress_score = min(100, payload.get("stress_level", 5) * 10)
        energy_score = np.clip((sleep_score + activity_score - stress_score) / 2, 0, 100)
        lifestyle_score = np.clip((activity_score + diet_score + sleep_score - stress_score) / 3, 0, 100)

        bmi_factor = np.clip((bmi - 18) * 7, 0, 100)
        inactivity = 100 - activity_score
        family = 100 if payload.get("family_history") else 0
        smoking = 100 if payload.get("smoking") else 20

        diabetes_risk = np.clip((bmi_factor + (100 - diet_score) + inactivity + family) / 4, 0, 100)
        heart_risk = np.clip((bmi_factor + stress_score + smoking + inactivity) / 4, 0, 100)
        bp_risk = np.clip((stress_score + (100 - diet_score) + bmi_factor) / 3, 0, 100)
        burnout_risk = np.clip((stress_score + (100 - sleep_score) + payload.get("work_hours", 8) * 7) / 3, 0, 100)
        sleep_disorder_risk = np.clip(((100 - sleep_score) + stress_score) / 2, 0, 100)
        fatigue_risk = np.clip(((100 - sleep_score) + stress_score + inactivity) / 3, 0, 100)
        diet_risk = np.clip((100 - diet_score), 0, 100)

        inferred_risk = self.model.predict(
            [[
                bmi,
                activity_score,
                sleep_score,
                diet_score,
                stress_score,
                1 if payload.get("family_history") else 0,
                1 if payload.get("smoking") else 0,
            ]]
        )[0]

        avg_risk = np.mean([diabetes_risk, heart_risk, bp_risk, inferred_risk])
        overall_health = np.clip((lifestyle_score + energy_score + (100 - avg_risk)) / 3, 0, 100)

        explainability = {
            "sleep": round(max(10, (100 - sleep_score) * 0.35), 1),
            "diet": round(max(10, (100 - diet_score) * 0.30), 1),
            "activity": round(max(10, inactivity * 0.35), 1),
        }

        return HealthMetrics(
            bmi=round(bmi, 2),
            activity_score=round(activity_score, 1),
            sleep_score=round(sleep_score, 1),
            diet_score=round(diet_score, 1),
            stress_score=round(stress_score, 1),
            energy_score=round(float(energy_score), 1),
            lifestyle_score=round(float(lifestyle_score), 1),
            diabetes_risk=round(float(diabetes_risk), 1),
            heart_risk=round(float(heart_risk), 1),
            bp_risk=round(float(bp_risk), 1),
            burnout_risk=round(float(burnout_risk), 1),
            sleep_disorder_risk=round(float(sleep_disorder_risk), 1),
            fatigue_risk=round(float(fatigue_risk), 1),
            diet_risk=round(float(diet_risk), 1),
            overall_health=round(float(overall_health), 1),
            explainability=explainability,
        )

    @staticmethod
    def timeline_projection(metrics: HealthMetrics) -> dict:
        continue_risk = np.clip(np.mean([metrics.diabetes_risk, metrics.heart_risk, metrics.bp_risk]) + 12, 0, 100)
        improve_risk = np.clip(continue_risk - 40, 0, 100)
        return {
            "three_months_continue": round(float(continue_risk), 1),
            "one_year_continue": round(float(min(100, continue_risk + 8)), 1),
            "three_months_improve": round(float(improve_risk), 1),
            "one_year_improve": round(float(max(0, improve_risk - 6)), 1),
        }

    @staticmethod
    def detect_silent_risk(recent_stress: list[int]) -> str | None:
        if len(recent_stress) < 5:
            return None
        trailing = recent_stress[:5]
        if all(s >= 7 for s in trailing):
            return "Your stress has stayed high for 5 days. Consider recovery mode today."
        return None

    @staticmethod
    def adaptive_goal(streak_days: int, previous_goal: int = 6000) -> int:
        if streak_days >= 7:
            return min(12000, previous_goal + 1000)
        if streak_days == 0:
            return max(3000, previous_goal - 1000)
        return previous_goal

    @staticmethod
    def _sleep_score(hours: float) -> float:
        if hours < 5:
            return 30
        if hours < 6:
            return 50
        if hours < 7:
            return 70
        if hours <= 8:
            return 90
        return 80


engine = RiskEngine()


def build_assistant_reply(question: str, metrics: HealthMetrics) -> str:
    q = question.lower()
    if "diet" in q:
        return (
            f"Your current diet score is {metrics.diet_score}/100. Focus on reducing sugar and junk meals, "
            "and target 2.5L+ water daily for a measurable risk drop."
        )
    if "risk" in q or "reduce" in q:
        return (
            f"Start with sleep and activity: your sleep impact is {metrics.explainability['sleep']}% and "
            f"activity impact is {metrics.explainability['activity']}%. A 7-day consistency sprint will help."
        )
    return (
        f"Your overall health score is {metrics.overall_health}. Prioritize one small habit today: hydration, "
        "15-minute walk, or a fixed bedtime."
    )


def generate_trend(logs: list[dict], key: str) -> list[dict]:
    return [
        {"date": entry["log_date"].isoformat() if isinstance(entry["log_date"], date) else entry["log_date"], "value": entry[key]}
        for entry in logs
    ]


def projection_dates() -> dict:
    today = date.today()
    return {
        "today": today.isoformat(),
        "three_months": (today + timedelta(days=90)).isoformat(),
        "one_year": (today + timedelta(days=365)).isoformat(),
    }
