from django.shortcuts import render, get_object_or_404
from .models import NosotrosPage, TopicPage
from .models import PilarPage


def nuestro_camino(request):
    page = get_object_or_404(NosotrosPage, enabled=True)
    return render(request, "nosotros/nuestro_camino.html", {"page": page})


def gobernanza(request):
    return render(request, "nosotros/gobernanza.html")


def principios_valores(request):
    return render(request, "nosotros/principios_valores.html")


def territorio(request):
    return render(request, "nosotros/territorio.html")


def pilar_detail(request, slug):
    page = get_object_or_404(
        PilarPage.objects.select_related("header").prefetch_related(
            "paragraphs", "quotes", "sidebar"
        ),
        slug=slug,
    )
    return render(request, f"nosotros/pilares/pilar_{slug}.html", {"page": page})


def topic_detail(request, slug):
    page = get_object_or_404(
        TopicPage.objects.select_related("header").prefetch_related(
            "paragraphs", "quotes", "sidebar"
        ),
        slug=slug,
    )
    # un solo template para todas:
    return render(request, "nosotros/topic_detail.html", {"page": page})


def pilar_bienestar(request):
    return render(request, "nosotros/pilares/pilar_bienestar.html")


def pilar_ecologia(request):
    return render(request, "nosotros/pilares/pilar_ecologia.html")


def pilar_economia(request):
    return render(request, "nosotros/pilares/pilar_economia.html")


def pilar_sociocultural(request):
    return render(request, "nosotros/pilares/pilar_sociocultural.html")

    # PILARES
