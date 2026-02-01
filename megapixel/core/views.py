from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def projects(request):
    category = request.GET.get('category')
    projects = Project.objects.all().order_by('-created_at')

    if category:
        projects = projects.filter(category=category)

    return render(request, 'projects.html', {
        'projects': projects,
        'project_categories': Project.CATEGORY_CHOICES
    })

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_detail.html', {'project': project})

@login_required
def profile(request):
    return render(request, 'profile.html')

def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        send_mail(
            subject=f"New message from {form.cleaned_data['name']}",
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['your_email@gmail.com'],
        )
        return render(request, 'contact.html', {'form': ContactForm(), 'success': True})

    return render(request, 'contact.html', {'form': form})

def contact(request):
    form = ContactForm(request.POST or None)

    if form.is_valid():
        admins = User.objects.filter(is_superuser=True).values_list('email', flat=True)

        send_mail(
            subject=f"New message from {form.cleaned_data['name']}",
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=list(admins),
            fail_silently=False,
        )

        return render(request, 'contact.html', {
            'form': ContactForm(),
            'success': True
        })

    return render(request, 'contact.html', {'form': form})