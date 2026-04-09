from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, EmailOTP, ContactMessage
from .forms import ContactForm
import random
import json
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .models import ClientGallery, BTSVideo

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def projects(request):

    category = request.GET.get('category')

    projects = Project.objects.all().order_by('-created_at')

    public_galleries = ClientGallery.objects.filter(is_public=True)

    if category:
        projects = projects.filter(category=category)

    from .models import BTSVideo
    bts_videos = BTSVideo.objects.all().order_by('-created_at')
    return render(request, 'projects.html', {
        'projects': projects,
        'project_categories': Project.CATEGORY_CHOICES,
        'public_galleries': public_galleries,
        'bts_videos': bts_videos,
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

            # Save message to database
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message,
            )

            try:
                send_mail(
                    subject=f"New contact from {name}",
                    message=message,
                    from_email=email,
                    recipient_list=["megapixelcreationss@gmail.com"],
                )
            except Exception as e:
                print("EMAIL ERROR:", e)

            success = True
            form = ContactForm()

    else:
        form = ContactForm()

    return render(
        request,
        "contact.html",
        {
            "form": form,
            "success": success,
        },
    )

def send_otp(request):

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

    try:

        data = json.loads(request.body)

        email = data.get("email")

        if not email:
            return JsonResponse(
                {"status": "error", "message": "Email required"}
            )

        # OTP spam protection
        recent = EmailOTP.objects.filter(email=email).order_by("-created_at").first()

        if recent and (timezone.now() - recent.created_at).seconds < 60:
            return JsonResponse(
                {"status": "error", "message": "Wait before requesting another OTP"}
            )

        otp = random.randint(100000, 999999)

        EmailOTP.objects.create(
            email=email,
            otp=otp,
        )

        try:
            send_mail(
                "Your OTP Code",
                f"Your OTP is {otp}",
                "megapixelcreationss@gmail.com",
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print("OTP EMAIL ERROR:", e)

        return JsonResponse({"status": "sent"})

    except Exception as e:

        print("OTP ERROR:", e)

        return JsonResponse(
            {"status": "error", "message": str(e)}
        )
 

def verify_otp(request):

    try:

        data = json.loads(request.body)

        email = data.get("email")
        otp = data.get("otp")

        record = EmailOTP.objects.filter(email=email, otp=otp).last()

        if record and timezone.now() - record.created_at < timedelta(minutes=5):

            record.delete()

            return JsonResponse({"status": "verified"})

        return JsonResponse({"status": "invalid"})

    except Exception as e:

        print("VERIFY OTP ERROR:", e)

        return JsonResponse(
            {"status": "error", "message": str(e)}
        )
    
def client_galleries(request):

    galleries = ClientGallery.objects.filter(is_public=True)
    return render(request, "client_galleries.html", {
        "galleries": galleries
    })

def client_gallery_detail(request, pk):
    gallery = get_object_or_404(
        ClientGallery,
        pk=pk,
        is_public=True
    )
    return render(request,"client_gallery_detail.html",{
        "gallery":gallery
    })
def public_gallery(request, pk):

    gallery = get_object_or_404(
        ClientGallery,
        pk=pk,
        is_public=True
    )

    return render(request,"public_gallery.html",{
        "gallery":gallery
    })
def bts_gallery(request):
    bts_videos = BTSVideo.objects.all().order_by('-created_at')
    return render(request, 'bts_gallery.html', {'bts_videos': bts_videos})