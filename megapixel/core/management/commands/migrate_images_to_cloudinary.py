from django.core.management.base import BaseCommand
from core.models import Project, ProjectImage

class Command(BaseCommand):
    help = "Re-save images so Cloudinary storage is used"

    def handle(self, *args, **kwargs):
        for p in Project.objects.all():
            if p.cover:
                p.cover.save(p.cover.name, p.cover.file, save=True)

        for img in ProjectImage.objects.all():
            if img.image:
                img.image.save(img.image.name, img.image.file, save=True)

        print("All images migrated to Cloudinary.")