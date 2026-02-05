# core/templatetags/gallery_headers.py
from django import template
from inicio.models import SectionHeader, Gallery  # <-- ajusta al app real

register = template.Library()


@register.inclusion_tag("components/participa_estancias_block.html", takes_context=True)
def gallery_headers_estancias(context, seccion, title="", subtitle="", limit=6):
    """
    Prioridad:
      1) SectionHeader(seccion=<value>, publicado=True) -> admin
      2) Parámetros title / subtitle del tag
      3) Defaults ("Estancias", "")
    """
    # Asegura que 'seccion' venga como value de choices (p.ej. 'participa_estancias')
    sh = SectionHeader.objects.filter(seccion=seccion, publicado=True).first()

    header_title = sh.title if sh and sh.title else (title or "Estancias")
    header_subtitle = sh.subtitle if sh and sh.subtitle else (subtitle or "")

    estancias = Gallery.objects.filter(seccion=seccion, publicado=True).order_by(
        "orden", "-creado"
    )[: int(limit)]

    return {
        # NOMBRES EXACTOS que usa tu parcial:
        "title": header_title,
        "subtitle": header_subtitle,
        "estancias": estancias,
        "request": context.get("request"),
    }
