import json
import random
from datetime import timedelta

from django.core.mail import send_mail
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import CategoryImage
from .models import CategoryImage

from .forms import ContactForm
from .models import (
    BTSVideo,
    ClientGallery,
    ClientGalleryImage,
    ContactMessage,
    EmailOTP,
    Project,
    ProjectImage,
)

# Main gallery categories shown in Prama's Gallery
PRAMA_CATEGORIES = {
    "wedding": {
        "title": "Wedding",
        "icon": "🥂",
        "description": "All wedding moments, rituals, emotions, and memories.",
    },
    "prewedding": {
        "title": "Pre-Wedding",
        "icon": "📸",
        "description": "Romantic sessions, stylish frames, and natural chemistry.",
    },
    "cinematography": {
        "title": "Cinematography",
        "icon": "🎬",
        "description": "Cinematic films with motion, emotion, and beautiful edits.",
    },
    "babyshoot": {
        "title": "Baby Shoot",
        "icon": "🍼",
        "description": "Cute, playful, and lovely baby photography moments.",
    },
    "advertisement": {
        "title": "Advertisement",
        "icon": "📢",
        "description": "Creative commercial and brand visuals.",
    },
    "corporate": {
        "title": "Corporate Shoot",
        "icon": "🏢",
        "description": "Professional portraits and business content.",
    },
}

PRAMA_CATEGORY_ORDER = [
    "wedding",
    "prewedding",
    "cinematography",
    "babyshoot",
    "advertisement",
    "corporate",
]


def home(request):
    featured_services = [
        {
            "title": "Wedding Photography",
            "slug": "wedding",
            "icon": "🥂",
            "image": "dummy/wedding.jpeg",
            "description": (
                "Creative wedding storytelling with candid moments, family emotions, "
                "and timeless portraits crafted for your memories."
            ),
        },
        {
            "title": "Pre-Wedding Photography",
            "slug": "prewedding",
            "icon": "📸",
            "image": "dummy/pre-wedding.jpeg",
            "description": (
                "Lifestyle pre-wedding sessions with natural chemistry, cinematic "
                "locations, and poses that feel personal and effortless."
            ),
        },
        {
            "title": "Cinematography",
            "slug": "cinematography",
            "icon": "🎬",
            "image": "dummy/cinematic.jpeg",
            "description": (
                "Cinematic wedding films with creative camera movement, intentional "
                "lighting, and emotional edits that feel like your own movie."
            ),
        },
        {
            "title": "Baby Shoot",
            "slug": "babyshoot",
            "icon": "🍼",
            "image": "dummy/baby.jpeg",
            "description": (
                "Adorable baby photography sessions capturing playful moments, "
                "cute expressions, and the pure joy of your little one."
            ),
        },
        {
            "title": "Advertisement",
            "slug": "advertisement",
            "icon": "📢",
            "image": "dummy/advertisement.jpeg",
            "description": (
                "Creative commercial photography and brand visuals that tell your "
                "story and connect with your audience."
            ),
        },
        {
            "title": "Corporate Shoot",
            "slug": "corporate",
            "icon": "🏢",
            "image": "dummy/corporate.jpeg",
            "description": (
                "Professional corporate photography for portraits, events, and "
                "business content that elevates your brand."
            ),
        },
        
    ]

    latest_images = ProjectImage.objects.order_by("-id")[:100]

    return render(
        request,
        "home.html",
        {
            "featured_services": featured_services,
            "latest_images": latest_images,
        },
    )


def about(request):
    return render(request, "about.html")


def projects(request):
    category = request.GET.get("category")

    projects_qs = Project.objects.all().order_by("-created_at")
    public_galleries = ClientGallery.objects.filter(is_public=True)
    bts_videos = BTSVideo.objects.all().order_by("-created_at")

    if category:
        projects_qs = projects_qs.filter(category=category)

    return render(
        request,
        "projects.html",
        {
            "projects": projects_qs,
            "project_categories": Project.CATEGORY_CHOICES,
            "public_galleries": public_galleries,
            "bts_videos": bts_videos,
        },
    )


def services(request):
    return render(request, "services.html")


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "project_detail.html", {"project": project})


def contact(request):
    success = False

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

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
            except Exception as exc:
                print("EMAIL ERROR:", exc)

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
            return JsonResponse({"status": "error", "message": "Email required"})

        recent = EmailOTP.objects.filter(email=email).order_by("-created_at").first()

        if recent and (timezone.now() - recent.created_at).seconds < 60:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Wait before requesting another OTP",
                }
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
        except Exception as exc:
            print("OTP EMAIL ERROR:", exc)

        return JsonResponse({"status": "sent"})

    except Exception as exc:
        print("OTP ERROR:", exc)
        return JsonResponse({"status": "error", "message": str(exc)})


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

    except Exception as exc:
        print("VERIFY OTP ERROR:", exc)
        return JsonResponse({"status": "error", "message": str(exc)})


# -------------------------
# NEW PRAMA'S GALLERY FLOW
# -------------------------

# ✅ STATIC COVER IMAGES FOR EACH CATEGORY
PRAMA_CATEGORY_COVERS = {
    "wedding": "dummy/wedding.jpeg",
    "prewedding": "dummy/pre-wedding.jpeg",
    "cinematography": "dummy/cinematic.jpeg",
    "babyshoot": "dummy/baby.jpeg",
    "advertisement": "dummy/advertisement.jpeg",
    "corporate": "dummy/corporate.jpeg",
}


def pramas_gallery(request):
    categories = []

    for slug in PRAMA_CATEGORY_ORDER:
        meta = PRAMA_CATEGORIES[slug]

        images_qs = CategoryImage.objects.filter(category=slug)

        categories.append({
            "slug": slug,
            "title": meta["title"],
            "icon": meta["icon"],
            "description": meta["description"],
            "cover_image": PRAMA_CATEGORY_COVERS.get(slug),  
            "image_count": images_qs.count(),
        })

    return render(request, "pramas_gallery.html", {
        "categories": categories,
    })



def pramas_gallery_category(request, slug):
    meta = PRAMA_CATEGORIES.get(slug)

    if not meta:
        raise Http404("Category not found")

    images = CategoryImage.objects.filter(category=slug).order_by("-id")

    return render(
        request,
        "pramas_gallery_detail.html",
        {
            "category": {
                "slug": slug,
                "title": meta["title"],
                "icon": meta["icon"],
                "description": meta["description"],
            },
            "images": images,
        },
    )


# -------------------------
# EXISTING CLIENT GALLERY FLOW
# -------------------------
def client_galleries(request):
    galleries = ClientGallery.objects.filter(is_public=True)
    return render(request, "client_galleries.html", {"galleries": galleries})


def client_gallery_detail(request, pk):
    gallery = get_object_or_404(ClientGallery, pk=pk, is_public=True)
    return render(request, "client_gallery_detail.html", {"gallery": gallery})


def public_gallery(request, pk):
    gallery = get_object_or_404(ClientGallery, pk=pk, is_public=True)
    return render(request, "public_gallery.html", {"gallery": gallery})


def bts_gallery(request):
    bts_videos = BTSVideo.objects.all().order_by("-created_at")
    return render(request, "bts_gallery.html", {"bts_videos": bts_videos})