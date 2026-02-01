from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Project, ProjectImage
from .forms import BulkImageUploadForm

@staff_member_required
def bulk_upload_images(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.method == 'POST':
        form = BulkImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            for img in request.FILES.getlist('images'):
                ProjectImage.objects.create(
                    project=project,
                    image=img
                )
            return redirect('/admin/core/project/%d/change/' % project.id)
    else:
        form = BulkImageUploadForm()

    return render(request, 'admin/bulk_upload.html', {
        'form': form,
        'project': project
    })
