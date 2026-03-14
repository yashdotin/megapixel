from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import EmailOTP
import random
import json

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

def services(request):
    return render(request, "services.html")

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_detail.html', {'project': project})




def contact(request):

    success = False

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():

            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            send_mail(
                subject=f"New contact from {name}",
                message=message,
                from_email=email,
                recipient_list=["yourgmail@gmail.com"],
            )

            success = True
            form = ContactForm()

    else:
        form = ContactForm()

    return render(request, "contact.html", {
        "form": form,
        "success": success
    })

def send_otp(request):

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)
    email = data.get("email")

    if not email:
        return JsonResponse({"error": "Email required"}, status=400)

    otp = random.randint(100000, 999999)

    EmailOTP.objects.create(
        email=email,
        otp=otp
    )

    send_mail(
        "Your OTP Verification Code",
        f"Your OTP is {otp}",
        "yourgmail@gmail.com",
        [email],
    )

    return JsonResponse({"status": "sent"})

def verify_otp(request):

    data = json.loads(request.body)

    email = data.get("email")
    otp = data.get("otp")

    record = EmailOTP.objects.filter(email=email, otp=otp).last()

    if record:
        return JsonResponse({"status": "verified"})
    else:
        return JsonResponse({"status": "invalid"})