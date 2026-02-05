from django.shortcuts import render
from .models import HeroSlide, ValorCard
from django.shortcuts import get_object_or_404
from .models import Gallery


def home(request):
    ctx = {
        "hero_slides": HeroSlide.objects.filter(publicado=True).order_by("orden"),
        "valores": ValorCard.objects.filter(publicado=True).order_by("orden")[:12],
    }
    return render(request, "inicio/home.html", ctx)


def gallery_detail(request, slug):
    gal = get_object_or_404(Gallery, slug=slug, publicado=True)
    items = gal.items.filter(publicado=True).order_by("orden", "-creado")
    return render(request, "inicio/gallery_detail.html", {"gal": gal, "items": items})
