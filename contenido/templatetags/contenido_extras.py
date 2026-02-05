# apps/contenido/templatetags/contenido_extras.py
from django import template
from django.db.models import Prefetch
from contenido.models import Placement, GalleryItem

register = template.Library()


@register.simple_tag
def get_placement(key):
    try:
        return Placement.objects.select_related("flyer", "gallery").get(
            key=key, activo=True
        )
    except Placement.DoesNotExist:
        return None


@register.inclusion_tag("contenido/_slider_proyectos.html")
def gallery_slider(key, limit=None, cta_text="Ver más", cta_url="#"):
    """
    Renderiza un slider (Owl) con la galería publicada del placement `key`.
    Usa: {% gallery_slider 'galeria_proyectos_dance' cta_text='Ver más' cta_url='/ruta/' %}
    """
    pl = (
        Placement.objects.select_related("gallery")
        .prefetch_related(
            Prefetch(
                # OJO: tu related_name es "items"
                "gallery__items",
                queryset=GalleryItem.objects.select_related("asset").order_by(
                    "orden", "id"
                ),
            )
        )
        .filter(key=key, activo=True)
        .first()
    )

    items = []
    if pl and pl.gallery and getattr(pl.gallery, "publicado", True):
        # Accede por el related_name "items"
        items = list(pl.gallery.items.all())
        # Filtra los que no tengan imagen por seguridad
        items = [gi for gi in items if gi.asset and gi.asset.imagen]
        if limit:
            items = items[: int(limit)]

    return {"items": items, "cta_text": cta_text, "cta_url": cta_url}
