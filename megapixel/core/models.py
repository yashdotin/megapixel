from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('wedding', 'Wedding'),
        ('prewedding', 'Pre-Wedding'),
        ('cinematography', 'Cinematography'),
        ('babyshoot', 'Baby Shoot'),
        ('advertisement', 'Advertisement'),
        ('corporate', 'Corporate Shoots'),

        # keeping your existing old categories so nothing breaks
        ('podcast', 'Podcast'),
        ('documentary', 'Documentary'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        blank=True
    )
    title = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    shoot_date = models.DateField(null=True, blank=True)
    camera_used = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    cover = CloudinaryField("cover", resource_type="auto", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Model for BTS mp4 videos
class BTSVideo(models.Model):

    title = models.CharField(max_length=200)
    cover = CloudinaryField("cover", resource_type="auto", blank=True, null=True)
    video = CloudinaryField("video", resource_type="video")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        related_name='images',
        on_delete=models.CASCADE
    )

    image = CloudinaryField("image", blank=True, null=True)

    def __str__(self):
        return f"{self.project.title} image"

class ContactMessage(models.Model):

    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EmailOTP(models.Model):

    email = models.EmailField()
    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class ClientGallery(models.Model):

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="client_galleries"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # show on portfolio/projects page
    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ClientGalleryImage(models.Model):

    gallery = models.ForeignKey(
        ClientGallery,
        related_name="images",
        on_delete=models.CASCADE
    )

    image = CloudinaryField("image")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gallery.title} image"
    
class CategoryImage(models.Model):
    CATEGORY_CHOICES = [
        ('wedding', 'Wedding'),
        ('prewedding', 'Pre-Wedding'),
        ('cinematography', 'Cinematography'),
        ('babyshoot', 'Baby Shoot'),
        ('advertisement', 'Advertisement'),
        ('corporate', 'Corporate Shoot'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = CloudinaryField("image")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} image"