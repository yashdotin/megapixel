from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html

from .admin_views import bulk_upload_images, bulk_upload_category_images
from .models import (
    CategoryImage,
    Project,
    ProjectImage,
    BTSVideo,
    ClientGallery,
    ClientGalleryImage,
)


@admin.register(BTSVideo)
class BTSVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "description")


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3
    max_num = 10


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "shoot_date", "image_count", "bulk_upload_link")
    list_filter = ("category",)
    search_fields = ("title", "client_name", "location")
    inlines = [ProjectImageInline]

    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = "Images"

    def bulk_upload_link(self, obj):
        if not obj.pk:
            return "Save first"
        url = reverse("admin:bulk_upload_images", args=[obj.id])
        return format_html('<a href="{}">📤 Upload Images</a>', url)

    bulk_upload_link.short_description = "Bulk Upload"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:project_id>/bulk-upload/",
                self.admin_site.admin_view(bulk_upload_images),
                name="bulk_upload_images",
            ),
        ]
        return custom_urls + urls


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "category")

    def category(self, obj):
        return obj.project.category


class ClientGalleryImageInline(admin.TabularInline):
    model = ClientGalleryImage
    extra = 10


@admin.register(ClientGallery)
class ClientGalleryAdmin(admin.ModelAdmin):
    inlines = [ClientGalleryImageInline]
    list_display = ("title", "client", "is_public")


@admin.register(ClientGalleryImage)
class ClientGalleryImageAdmin(admin.ModelAdmin):
    list_display = ("gallery", "uploaded_at")


@admin.register(CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
    list_display = ("category", "uploaded_at", "bulk_upload_link")
    list_filter = ("category",)
    search_fields = ("category",)
    ordering = ("-uploaded_at",)

    def bulk_upload_link(self, obj):
        url = reverse("admin:core_categoryimage_bulk_upload")
        return format_html('<a class="button" href="{}">📤 Bulk Upload</a>', url)

    bulk_upload_link.short_description = "Upload"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "bulk-upload/",
                self.admin_site.admin_view(bulk_upload_category_images),
                name="core_categoryimage_bulk_upload",
            ),
        ]
        return custom_urls + urls