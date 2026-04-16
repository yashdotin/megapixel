import json
from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import DailyHealthLog, HealthAlert, UserHealthProfile
from .services import (
    build_assistant_reply,
    engine,
    generate_trend,
    projection_dates,
)


def _payload_from_profile(profile: UserHealthProfile) -> dict:
    return {
        "height_cm": profile.height_cm,
        "weight_kg": profile.weight_kg,
        "activity_level": profile.activity_level,
        "sleep_hours": profile.sleep_hours,
        "junk_food_frequency": profile.junk_food_frequency,
        "sugar_intake": profile.sugar_intake,
        "water_liters": profile.water_liters,
        "stress_level": profile.stress_level,
        "work_hours": profile.work_hours,
        "family_history": profile.family_history,
        "smoking": profile.smoking,
    }


@login_required
def health_home(request):
    return render(request, "health/index.html")


@login_required
@require_POST
def submit_onboarding(request):
    data = json.loads(request.body)
    profile, _ = UserHealthProfile.objects.update_or_create(
        user=request.user,
        defaults={
            "age": data.get("age", 25),
            "gender": data.get("gender", "unknown"),
            "height_cm": data.get("height_cm", 170),
            "weight_kg": data.get("weight_kg", 70),
            "activity_level": data.get("activity_level", "medium"),
            "exercise_days": data.get("exercise_days", 2),
            "sleep_hours": data.get("sleep_hours", 7),
            "sleep_quality": data.get("sleep_quality", "average"),
            "junk_food_frequency": data.get("junk_food_frequency", "medium"),
            "sugar_intake": data.get("sugar_intake", "medium"),
            "water_liters": data.get("water_liters", 2.0),
            "stress_level": data.get("stress_level", 5),
            "mood": data.get("mood", "neutral"),
            "work_hours": data.get("work_hours", 8),
            "smoking": data.get("smoking", False),
            "alcohol": data.get("alcohol", "low"),
            "family_history": data.get("family_history", False),
            "existing_conditions": data.get("existing_conditions", ""),
        },
    )

    metrics = engine.compute_metrics(_payload_from_profile(profile))
    return JsonResponse({"status": "ok", "health_profile": metrics.__dict__})


@login_required
@require_POST
def submit_daily_log(request):
    data = json.loads(request.body)
    profile = UserHealthProfile.objects.get(user=request.user)

    log_date = date.fromisoformat(data.get("log_date", date.today().isoformat()))
    log, _ = DailyHealthLog.objects.update_or_create(
        profile=profile,
        log_date=log_date,
        defaults={
            "sleep_hours": data.get("sleep_hours", profile.sleep_hours),
            "water_liters": data.get("water_liters", profile.water_liters),
            "stress_level": data.get("stress_level", profile.stress_level),
            "steps": data.get("steps", 3000),
            "diet_note": data.get("diet_note", ""),
            "feeling": data.get("feeling", ""),
        },
    )

    if profile.last_log_date and (log_date - profile.last_log_date).days == 1:
        profile.streak_days += 1
    elif profile.last_log_date != log_date:
        profile.streak_days = 1

    profile.last_log_date = log_date
    profile.xp_points += 10
    profile.sleep_hours = log.sleep_hours
    profile.water_liters = log.water_liters
    profile.stress_level = log.stress_level
    profile.save()

    recent_stress = list(profile.logs.values_list("stress_level", flat=True)[:5])
    silent_message = engine.detect_silent_risk(recent_stress)
    if silent_message:
        HealthAlert.objects.create(profile=profile, message=silent_message, severity="high")

    next_goal = engine.adaptive_goal(profile.streak_days)
    return JsonResponse(
        {
            "status": "ok",
            "xp": profile.xp_points,
            "streak": profile.streak_days,
            "next_steps_goal": next_goal,
            "silent_alert": silent_message,
        }
    )


@login_required
def dashboard_data(request):
    profile, _ = UserHealthProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "age": 25,
            "gender": "unknown",
            "height_cm": 170,
            "weight_kg": 70,
            "activity_level": "medium",
        },
    )
    metrics = engine.compute_metrics(_payload_from_profile(profile))
    projection = engine.timeline_projection(metrics)
    logs = list(profile.logs.values("log_date", "sleep_hours", "stress_level", "water_liters")[:14])
    trend = {
        "stress": generate_trend(logs, "stress_level"),
        "sleep": generate_trend(logs, "sleep_hours"),
        "water": generate_trend(logs, "water_liters"),
    }

    return JsonResponse(
        {
            "metrics": metrics.__dict__,
            "timeline": projection,
            "timeline_dates": projection_dates(),
            "xp": profile.xp_points,
            "streak": profile.streak_days,
            "alerts": list(profile.alerts.values("message", "severity", "created_at")[:5]),
            "trend": trend,
        }
    )


@login_required
@require_POST
def assistant_chat(request):
    data = json.loads(request.body)
    question = data.get("message", "")
    profile = UserHealthProfile.objects.get(user=request.user)
    metrics = engine.compute_metrics(_payload_from_profile(profile))
    reply = build_assistant_reply(question, metrics)
    return JsonResponse({"reply": reply})
