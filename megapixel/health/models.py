from django.conf import settings
from django.db import models


class UserHealthProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20)
    height_cm = models.FloatField()
    weight_kg = models.FloatField()
    activity_level = models.CharField(max_length=20)
    exercise_days = models.PositiveIntegerField(default=0)
    sleep_hours = models.FloatField(default=7)
    sleep_quality = models.CharField(max_length=20, default="average")
    junk_food_frequency = models.CharField(max_length=20, default="medium")
    sugar_intake = models.CharField(max_length=20, default="medium")
    water_liters = models.FloatField(default=2.0)
    stress_level = models.PositiveIntegerField(default=5)
    mood = models.CharField(max_length=20, default="neutral")
    work_hours = models.PositiveIntegerField(default=8)
    smoking = models.BooleanField(default=False)
    alcohol = models.CharField(max_length=20, default="low")
    family_history = models.BooleanField(default=False)
    existing_conditions = models.CharField(max_length=255, blank=True)

    xp_points = models.PositiveIntegerField(default=0)
    streak_days = models.PositiveIntegerField(default=0)
    last_log_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DailyHealthLog(models.Model):
    profile = models.ForeignKey(UserHealthProfile, on_delete=models.CASCADE, related_name="logs")
    log_date = models.DateField()
    sleep_hours = models.FloatField(default=7)
    water_liters = models.FloatField(default=2)
    stress_level = models.PositiveIntegerField(default=5)
    steps = models.PositiveIntegerField(default=3000)
    diet_note = models.CharField(max_length=255, blank=True)
    feeling = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-log_date"]
        unique_together = ("profile", "log_date")


class HealthAlert(models.Model):
    profile = models.ForeignKey(UserHealthProfile, on_delete=models.CASCADE, related_name="alerts")
    message = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, default="medium")
    created_at = models.DateTimeField(auto_now_add=True)
