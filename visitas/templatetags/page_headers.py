# core/templatetags/page_headers.py
from django import template
from django.templatetags.static import static
from django.conf import settings
from core.models import PageHeader

register = template.Library()


@register.inclusion_tag("inner_header.html", takes_context=True)
def page_header(context, slug, default_title="", default_subtitle=""):
    header = PageHeader.objects.filter(slug=slug, is_active=True).first()
    bg_fallback = getattr(
        settings, "BG_FALLBACK", static("participa/images/cabeza-voluntariado.png")
    )
    breadcrumbs = context.get("breadcrumbs", [])
    return {
        "header": header,
        "BG_FALLBACK": bg_fallback,
        "default_title": default_title,
        "default_subtitle": default_subtitle,
        "breadcrumbs": breadcrumbs,
    }
