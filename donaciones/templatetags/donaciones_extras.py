# apps/donaciones/templatetags/donaciones_extras.py
from django import template
from donaciones.models import DonacionSection

register = template.Library()


@register.inclusion_tag("donaciones/_donation_callout.html")
def donation_callout(slug):
    section = (
        DonacionSection.objects.prefetch_related("montos")
        .filter(slug=slug, publicado=True)
        .first()
    )
    return {"section": section}


# Custom template tags para donaciones
