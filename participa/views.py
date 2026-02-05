from django.shortcuts import render, get_object_or_404
from .models import ParticipaPage, Estancia
from .models import VoluntariadoPage  # tu modelo de la captura
from django.templatetags.static import static

# participa/views.py
from django.http import Http404


def voluntariado(request):
    pagina = VoluntariadoPage.objects.filter(publicado=True).first()
    if not pagina:
        raise Http404("Página de Voluntariado no configurada")

    # Helper para elegir el primer campo existente/no vacío
    def pick(*names):
        for n in names:
            if hasattr(pagina, n):
                val = getattr(pagina, n)
                if val:
                    return val
        return None

    # Título: intenta con varios nombres posibles
    titulo = pick("title", "titulo", "name", "nombre", "heading") or "Voluntariado"

    # Imagen de cabecera: prioridad background → thumb → hero → imagen → image
    imagen_field = pick("background", "thumb", "hero", "imagen", "image")

    # Construir URL segura (si es FileField/ImageField usa .url; si es string úsalo directo)
    fallback = static("participa/images/cabeza-voluntariado.png")
    if imagen_field:
        try:
            bg_url = imagen_field.url  # ImageField/FileField
        except Exception:
            bg_url = str(imagen_field)  # Por si vino como string
    else:
        bg_url = fallback

    breadcrumbs = [
        {"label": "Inicio", "url": "/"},
        {"label": "Participa", "url": "/participa/"},
        {"label": "Voluntariado", "url": None},
    ]

    ctx = {
        "header_title": titulo,
        "header_bg_url": bg_url,
        "BG_FALLBACK": fallback,
        "breadcrumbs": breadcrumbs,
        "pagina": pagina,
    }
    return render(request, "participa/voluntariado/voluntariado.html", ctx)


def estancias_list(request):
    page = ParticipaPage.objects.select_related("header").first()
    estancias = Estancia.objects.filter(
        seccion="participa_estancias", publicado=True
    ).order_by("orden", "-creado")
    return render(
        request,
        "participa/estancias/estancias_list.html",
        {"estancias": estancias, "page": page},
    )


def estancia_detail(request, slug):
    page = ParticipaPage.objects.select_related("header").first()
    e = get_object_or_404(Estancia, slug=slug, publicado=True)
    fotos = e.fotos.filter(publicado=True).order_by("orden", "-creado")
    specs = e.specs.all().order_by("orden", "id")
    return render(
        request,
        "participa/estancias/estancia_detail.html",
        {
            "page": page,
            "e": e,
            "fotos": fotos,
            "specs": specs,
            "phone": e.phone_whatsapp or "",
        },
    )


def donaciones(request, id):
    return render(request, "donaciones/donaciones.html")
