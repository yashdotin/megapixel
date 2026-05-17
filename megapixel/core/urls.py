from django.urls import path
from .views import home, about, projects, project_detail, contact, bts_gallery
from accounts.views import profile
from . import views

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("projects/", projects, name="projects"),
    path("projects/<int:pk>/", project_detail, name="project_detail"),
    path("contact/", contact, name="contact"),
    path("profile/", profile, name="profile"),
    path("services/", views.services, name="services"),

    path("send-otp/", views.send_otp),
    path("verify-otp/", views.verify_otp),

    # Client galleries (unchanged)
    path("client-galleries/", views.client_galleries, name="client_galleries"),
    path("client-gallery/<int:pk>/", views.client_gallery_detail, name="client_gallery_detail"),

    # ✅ PRAMA'S GALLERY
    path("my-galleries/", views.pramas_gallery, name="pramas_gallery"),
    path("my-galleries/<slug:slug>/", views.pramas_gallery_category, name="pramas_gallery_category"),

    path("bts/", bts_gallery, name="bts_gallery"),
    path("reels/", views.reels_gallery, name="reels_gallery"),
]