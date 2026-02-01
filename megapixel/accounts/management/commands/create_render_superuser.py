from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Create superuser on Render if not exists"

    def handle(self, *args, **kwargs):
        username = "megapixel_admin"
        email = "admin@megapixel.com"
        password = "Admin@123"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write("✅ Superuser created")
        else:
            self.stdout.write("ℹ️ Superuser already exists")
