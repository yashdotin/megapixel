from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)

    shoot_date = models.DateField(null=True, blank=True)
    camera_used = models.CharField(max_length=200, blank=True)

    CATEGORY_CHOICES = [
    ('wedding', 'Wedding'),
    ('birthday', 'Birthday'),
    ('prewedding', 'Pre-Wedding'),
    ('engagement', 'Engagement'),
    ('portrait', 'Portrait'),
    ('travel', 'Travel'),
    ('corporate', 'Corporate Event'),
    ('concert', 'Concert / Stage Show'),
    ('fashion', 'Fashion Shoot'),
    ('product', 'Product Shoot'),
    ('other', 'Other Event'),
]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        blank=True
    )

    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='projects/covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/images/', blank=True, null=True)


    def __str__(self):
        return f"{self.project.title} image"
