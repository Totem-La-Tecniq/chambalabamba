from django import template
from django.db.models import Q
from tienda.models import Producto, ProductoCategoria

# NUEVO:
try:
    from inicio.models import SectionHeader
except Exception:
    SectionHeader = None

register = template.Library()


def productos_por_categoria(cat_key: str, limit=None):
    """Devuelve productos publicados por slug/nombre de categoría."""
    cat_key = (cat_key or "").strip()
    if not cat_key:
        return Producto.objects.none()

    qs = (
        Producto.objects.filter(publicado=True)
        .filter(
            Q(categoria__slug=cat_key)
            | Q(categoria__slug__iexact=cat_key)
            | Q(categoria__nombre__iexact=cat_key)
        )
        .select_related("categoria")
        .order_by("orden", "-creado")
    )

    # Prefetch seguro (si no tienes related_name='imagenes', usa el set por defecto)
    try:
        Producto._meta.get_field("imagenes")
        qs = qs.prefetch_related("imagenes")
    except Exception:
        qs = qs.prefetch_related("productoimagen_set")

    if limit:
        try:
            limit = int(limit)
            if limit > 0:
                qs = qs[:limit]
        except (TypeError, ValueError):
            pass
    return qs


@register.inclusion_tag("tienda/_products_tabs.html")
def products_tabs(
    header_h5=None,  # <-- default None para permitir override
    header_h2=None,  # <-- default None para permitir override
    categorias="",
    limit=8,
    hide_header=False,
):
    tabs = []
    # ==== NUEVO: intentar leer títulos desde SectionHeader si no vinieron por parámetro ====
    if (header_h2 is None or header_h5 is None) and SectionHeader is not None:
        hdr = SectionHeader.objects.filter(
            seccion="tienda_tabs", publicado=True
        ).first()
        if hdr:
            if header_h2 is None:
                header_h2 = hdr.title or "Productos"
            if header_h5 is None:
                header_h5 = hdr.subtitle or ""
    # Fallbacks seguros
    header_h2 = header_h2 or "Productos"
    header_h5 = header_h5 or "Visita nuestra tienda"
    # ==== /NUEVO ====

    if categorias:
        # ... igual ...
        pass
    else:
        cats = (
            ProductoCategoria.objects.filter(publicado=True, productos__publicado=True)
            .order_by("orden", "nombre")
            .distinct()
        )
        for c in cats:
            tabs.append(
                {
                    "id": c.slug,
                    "title": c.nombre,
                    "items": productos_por_categoria(c.slug, limit),
                }
            )

    return {
        "header_h5": header_h5,
        "header_h2": header_h2,
        "tabs": tabs,
        "hide_header": hide_header,  # ya lo tienes
    }
