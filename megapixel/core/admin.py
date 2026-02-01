from django.contrib import admin
from .models import Project, ProjectImage
from django.urls import path
from django.utils.html import format_html
from django.shortcuts import redirect
from .admin_views import bulk_upload_images

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3
    max_num = 10
    can_delete = True
    verbose_name = "Gallery Image"
    verbose_name_plural = "Gallery Images"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'shoot_date', 'bulk_upload_link')
    list_filter = ('category',)
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