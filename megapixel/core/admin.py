from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from django.shortcuts import redirect
from .admin_views import bulk_upload_images
from .models import Project, ProjectImage, BTSVideo, ClientGallery, ClientGalleryImage

# Register BTSVideo for admin management
@admin.register(BTSVideo)
class BTSVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')

class ClientGalleryImageInline(admin.TabularInline):
    model = ClientGalleryImage
    extra = 10


class ClientGalleryAdmin(admin.ModelAdmin):
    inlines = [ClientGalleryImageInline]

admin.site.register(ClientGallery, ClientGalleryAdmin)


admin.site.register(ClientGalleryImage)

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3
    max_num = 10
    can_delete = True
    verbose_name = "Gallery Image"
    verbose_name_plural = "Gallery Images"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'shoot_date', 'bulk_upload_link')
    list_filter = ()
    search_fields = ('title', 'client_name', 'location')
    inlines = [ProjectImageInline]

    def bulk_upload_link(self, obj):
        return format_html(
            '<a href="/admin/core/project/{}/bulk-upload/">Bulk Upload</a>',
            obj.id
        )
    bulk_upload_link.short_description = "Bulk Upload Images"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:project_id>/bulk-upload/',
                self.admin_site.admin_view(bulk_upload_images),
                name='bulk_upload_images'
            ),
        ]
        return custom_urls + urls