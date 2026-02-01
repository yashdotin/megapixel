from django.apps import AppConfig
import os

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    def ready(self):
        if os.getenv("DJANGO_SUPERUSER_USERNAME") and os.getenv("DJANGO_SUPERUSER_EMAIL") and os.getenv("DJANGO_SUPERUSER_PASSWORD"):
            from .signals import create_user_profile    
            create_user_profile()
            
