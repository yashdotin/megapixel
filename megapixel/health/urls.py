from django.urls import path

from . import views

urlpatterns = [
    path("", views.health_home, name="health_home"),
    path("api/onboarding/", views.submit_onboarding, name="submit_onboarding"),
    path("api/log/", views.submit_daily_log, name="submit_daily_log"),
    path("api/dashboard/", views.dashboard_data, name="dashboard_data"),
    path("api/assistant/", views.assistant_chat, name="assistant_chat"),
]
