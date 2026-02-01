import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "megapixel.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = os.environ.get("DJANGO_SUPERUSER_USERNAME", "megapixel_admin")
EMAIL = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@megapixel.com")
PASSWORD = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "change-this-password")

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print("✅ Superuser created")
else:
    print("ℹ️ Superuser already exists")
