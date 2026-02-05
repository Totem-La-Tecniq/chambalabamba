# cooperaciones/templatetags/coops_extras.py
from django import template
from cooperaciones.models import Cooperacion
from inicio.models import SectionHeader  # 👈 leeremos del admin de Inicio

register = template.Library()


@register.inclusion_tag("cooperaciones/_home_cooperaciones.html")
def _home_cooperaciones(
    seccion_key="home_cooperaciones", subtitle=None, title=None, limit=None
):
    # Lee configuración desde SectionHeader si existe y está publicado
    header = (
        SectionHeader.objects.filter(seccion=seccion_key, publicado=True)
        .only("title", "subtitle", "limit")
        .first()
    )

    if header:
        if not title:
            title = header.title or title
        if not subtitle:
            subtitle = header.subtitle or subtitle
        if limit is None:
            limit = header.limit

    # Defaults si nada vino del admin ni de la llamada
    if title is None:
        title = "Cooperaciones"
    if subtitle is None:
        subtitle = "Alianzas que nos potencian"
    if limit is None:
        limit = 12

    coops = (
        Cooperacion.objects.filter(publicado=True)
        .only("slug", "nombre", "logo", "portada", "excerpt", "orden", "creado")
        .order_by("orden", "-creado")[: int(limit)]
    )

    return {"coops": coops, "subtitle": subtitle, "title": title}
