from django.shortcuts import render, get_object_or_404
from .models import (
    Festival,
    TallerDetail,
    TalleresPage,
    FestivalesPage,
    ArtesPage,
    EscuelaPage,
    RetirosPage,
    TerapiasPage,
)

# Create your views here.


def escuela_viva(request):
    page_content = EscuelaPage.objects.first()
    return render(request, "eventos/escuela.html", {"page": page_content})


def talleres(request):
    talleres = TallerDetail.objects.all().order_by("-id")
    page_content = TalleresPage.objects.first()
    return render(
        request, "eventos/talleres.html", {"talleres": talleres, "page": page_content}
    )


def taller_detail(request, slug):
    taller = get_object_or_404(TallerDetail, slug=slug)
    return render(request, "eventos/taller_detail.html", {"taller": taller})


def retiros(request):
    page_content = RetirosPage.objects.first()
    return render(request, "eventos/retiros.html", {"page": page_content})


def artes(request):
    page_content = ArtesPage.objects.first()
    return render(request, "eventos/artes.html", {"page": page_content})


def terapias(request):
    page_content = TerapiasPage.objects.first()
    return render(request, "eventos/terapias.html", {"page": page_content})


def festivales(request):
    festivales = Festival.objects.all().order_by("-id")
    page_content = FestivalesPage.objects.first()
    return render(
        request,
        "eventos/festivales.html",
        {"festivales": festivales, "page": page_content},
    )


def festival_detail(request, slug):
    festival = get_object_or_404(Festival, slug=slug)
    return render(request, "eventos/festival_detail.html", {"festival": festival})
