from django.urls import path

from django.contrib.auth import views as auth_views
from .views import signup, edit_profile

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]
