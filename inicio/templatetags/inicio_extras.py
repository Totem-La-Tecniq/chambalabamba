from django import template
from inicio.models import Gallery, SectionHeader

register = template.Library()


@register.inclusion_tag("inicio/_gallery_headers_component.html")
def gallery_headers(seccion, title=None, subtitle=None, limit=None):
    qs = (
        Gallery.objects.filter(seccion=seccion, publicado=True)
        .exclude(portada="")
        .order_by("orden", "-creado")
    )
    if limit:
        try:
            qs = qs[: int(limit)]
        except (TypeError, ValueError):
            pass

    # OVERRIDE desde BD si hay SectionHeader publicado para esa sección
    header = SectionHeader.objects.filter(seccion=seccion, publicado=True).first()
    if header:
        if not title:
            title = header.title
        if not subtitle:
            subtitle = header.subtitle

    return {"galerias": qs, "title": title, "subtitle": subtitle}
