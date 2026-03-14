from django.urls import path
from .views import home, about, projects, project_detail, contact
from accounts.views import profile
from . import views


urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('projects/', projects, name='projects'),
    path('projects/<int:pk>/', project_detail, name='project_detail'),
    path('contact/', contact, name='contact'),
    path('profile/', profile, name='profile'),
    path('services/', views.services, name='services'),
    path("send-otp/",views.send_otp),
    path("verify-otp/",views.verify_otp),
]
