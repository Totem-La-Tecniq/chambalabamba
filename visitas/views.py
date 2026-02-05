# apps/visitas/views.py
from django.shortcuts import get_object_or_404, render
from .models import VisitsLanding, GuidedVisit


def visitas_index(request):
    landing = VisitsLanding.objects.filter(publicado=True).first()
    visitas = (
        GuidedVisit.objects.filter(publicado=True)
        .prefetch_related("fotos")
        .order_by("orden", "titulo")
    )

    header = {
        "title": landing.title if landing else "Visitas guiadas",
        "background": landing.background if landing and landing.background else None,
    }
    breadcrumbs = [
        {"label": "Inicio", "url": "/"},
        {"label": "Visitas", "url": "/visitas/"},
        {"label": "Visitas guiadas", "url": None},
    ]
    return render(
        request,
        "visitas-guiadas.html",
        {
            "landing": landing,
            "visitas": visitas,
            "header": header,
            "breadcrumbs": breadcrumbs,
        },
    )


def visita_detail(request, slug):
    visita = get_object_or_404(
        GuidedVisit.objects.prefetch_related("fotos"), slug=slug, publicado=True
    )
    # inner header del detalle
    bg = visita.inner_bg_override or visita.portada
    if not bg:
        first = next((f for f in visita.fotos.all() if f.publicado), None)
        bg = first.imagen if first else None

    header = {"title": visita.titulo, "background": bg}
    breadcrumbs = [
        {"label": "Inicio", "url": "/"},
        {"label": "Visitas", "url": "/visitas/"},
        {"label": "Visitas guiadas", "url": "/visitas/visitas/"},
        {"label": visita.titulo, "url": None},
    ]
    return render(
        request,
        "event-details.html",
        {
            "visita": visita,
            "header": header,
            "breadcrumbs": breadcrumbs,
        },
    )
