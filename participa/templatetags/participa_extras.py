# participa/templatetags/participa_extras.py
from django import template

register = template.Library()

# --------- Imports tolerantes ---------
try:
    # si existen en tu app participa
    from participa.models import (
        Estancia,
        InstaGallery,
        ProyectoVoluntariado,
        VoluntariadoPage,
    )
except Exception:
    Estancia = InstaGallery = ProyectoVoluntariado = VoluntariadoPage = None

try:
    # tu app real de cooperaciones
    from cooperaciones.models import Cooperacion
except Exception:
    Cooperacion = None

# NEW: header administrable (ajusta el import al app donde esté tu SectionHeader)
try:
    from inicio.models import SectionHeader
except Exception:
    SectionHeader = None


# ====== ESTANCIAS (admin-override para title/subtitle) ======
@register.inclusion_tag("participa/estancias/_gallery_headers_estancias.html")
def gallery_headers_estancias(
    seccion="participa_estancias",
    title=None,
    subtitle=None,
    limit=None,
    only_with_portada=True,
):
    """
    Prioridad de título/subtítulo:
      1) SectionHeader(seccion=<seccion>, publicado=True) del admin
      2) Parámetros title / subtitle pasados al tag
      3) Defaults: "Estancias" / ""
    Nota: 'seccion' debe usar el VALUE de tus choices, p.ej. 'participa_estancias'.
    """
    # Query de estancias (como ya lo tenías)
    if Estancia is None:
        qs = []
    else:
        qs = Estancia.objects.filter(publicado=True).order_by("orden", "-creado")
        if hasattr(Estancia, "seccion") and seccion:
            qs = qs.filter(seccion=seccion)
        if only_with_portada:
            qs = qs.exclude(portada="").exclude(portada__isnull=True)
        if limit:
            try:
                qs = qs[: int(limit)]
            except (TypeError, ValueError):
                pass

    # Header administrable (si el modelo existe)
    admin_title = admin_subtitle = None
    if SectionHeader is not None and seccion:
        sh = SectionHeader.objects.filter(seccion=seccion, publicado=True).first()
        if sh:
            # Soporta both title/titulo, subtitle/subtitulo
            admin_title = getattr(sh, "title", None) or getattr(sh, "titulo", None)
            admin_subtitle = getattr(sh, "subtitle", None) or getattr(
                sh, "subtitulo", None
            )

    # Resolución final
    final_title = admin_title or title or "Estancias"
    final_subtitle = admin_subtitle or subtitle or ""

    return {"estancias": qs, "title": final_title, "subtitle": final_subtitle}


# ====== INSTAGRAM GRID (si lo usas) ======
@register.inclusion_tag("participa/_insta_grid.html")
def participa_instagram(slug=None):
    if InstaGallery is None:
        return {"insta": None}
    if slug:
        gal = InstaGallery.objects.filter(
            publicado=True, seccion="participa_instagram", titulo=slug
        ).first()
    else:
        gal = InstaGallery.objects.filter(
            publicado=True, seccion="participa_instagram"
        ).first()
    return {"insta": gal}


# ====== COOPERACIONES (ÚNICA definición, con seccion) ======
@register.inclusion_tag(
    "participa/_cooperaciones.html", takes_context=False, name="participa_cooperaciones"
)
def participa_cooperaciones(
    title=None, subtitle=None, limit=None, seccion=None, order="orden,-creado"
):
    """
    Uso:
      {% participa_cooperaciones title="Cooperaciones" subtitle="Alianzas que nos potencian" limit=12 seccion="voluntariado" %}
    """
    qs = []
    if Cooperacion is not None:
        qs = Cooperacion.objects.all()
        # publicado=True si existe
        try:
            qs = qs.filter(publicado=True)
        except Exception:
            pass

        # filtro por seccion/categoria/tags si el modelo lo soporta
        if seccion:
            for candidate in (
                {"seccion": seccion},
                {"seccion__slug": seccion},
                {"categoria__slug": seccion},
                {"categoria__nombre__iexact": seccion},
                {"tags__name__iexact": seccion},
            ):
                try:
                    qs = qs.filter(**candidate)
                    break
                except Exception:
                    continue

        # orden tolerante
        try:
            fields = [f.strip() for f in (order or "").split(",") if f.strip()]
            if fields:
                qs = qs.order_by(*fields)
        except Exception:
            pass

        # límite
        try:
            if limit:
                qs = qs[: int(limit)]
        except Exception:
            pass

    return {"title": title, "subtitle": subtitle, "cooperaciones": qs}


# ====== SIDEBAR PROYECTOS VOLUNTARIADO ======
@register.inclusion_tag("participa/voluntariado/_sidebar_proyectos_voluntariado.html")
def voluntariado_sidebar_projects(limit=10, title=None):
    if ProyectoVoluntariado is None:
        return {"proyectos": [], "title": title}
    qs = ProyectoVoluntariado.objects.filter(publicado=True).order_by(
        "orden", "nombre"
    )[: int(limit)]
    return {"proyectos": qs, "title": title}


# ====== SINGLETON PAGE ======
@register.simple_tag
def voluntariado_page():
    """Uso en templates: {% voluntariado_page as vp %}"""
    if VoluntariadoPage is None:
        return None
    try:
        return (
            VoluntariadoPage.objects.filter(publicado=True).first()
            or VoluntariadoPage.get_solo()
        )
    except Exception:
        return None
