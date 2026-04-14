from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import BulkImageUploadForm, BulkCategoryImageUploadForm
from .models import Project, ProjectImage, CategoryImage


@staff_member_required
def bulk_upload_images(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = BulkImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            images = request.FILES.getlist('images')

            if not images:
                messages.error(request, "Please select images.")
                return redirect(request.path)

            count = 0
            for img in images:
                ProjectImage.objects.create(
                    project=project,
                    image=img
                )
                count += 1

            messages.success(request, f"{count} images uploaded successfully 🚀")
            return redirect(reverse("admin:core_project_change", args=[project.id]))
    else:
        form = BulkImageUploadForm()

    return render(request, 'admin/bulk_upload.html', {
        'form': form,
        'project': project
    })


@staff_member_required
def bulk_upload_category_images(request):
    if request.method == 'POST':
        form = BulkCategoryImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            category = form.cleaned_data["category"]
            images = request.FILES.getlist("images")

            if not images:
                messages.error(request, "Please select images.")
                return redirect(request.path)

            count = 0
            for img in images:
                CategoryImage.objects.create(
                    category=category,
                    image=img
                )
                count += 1

            messages.success(
                request,
                f"{count} category image(s) uploaded successfully 🚀"
            )
            return redirect(reverse("admin:core_categoryimage_changelist"))
    else:
        form = BulkCategoryImageUploadForm()

    return render(request, "admin/category_bulk_upload.html", {
        "form": form
    })