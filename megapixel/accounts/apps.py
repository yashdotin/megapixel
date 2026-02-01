from django.apps import AppConfig
import os

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from django.contrib.auth.models import User

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if username and password:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email}
            )

            # 🔥 FORCE permissions (THIS IS THE FIX)
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
