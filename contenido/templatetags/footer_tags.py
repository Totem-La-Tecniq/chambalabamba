# contenido/templatetags/footer_tags.py
from django import template
from django.urls import reverse, NoReverseMatch
from contenido.models import FooterSettings, FooterMenu
import json
import ast

register = template.Library()


def _parse_kwargs(raw):
    """Acepta JSON, 'null'/'none'/vacío y también dict con comillas simples."""
    if not raw:
        return {}
    s = str(raw).strip()
    if s.lower() in {"null", "none", ""}:
        return {}
    # 1) intenta JSON
    try:
        return json.loads(s)
    except Exception:
        pass
    # 2) intenta literal_eval (por si usaron comillas simples)
    try:
        val = ast.literal_eval(s)
        if isinstance(val, dict):
            return val
    except Exception:
        pass
    return {}


@register.inclusion_tag("partials/sub_footer_info.html", takes_context=True)
def render_footer(context):
    about = FooterSettings.objects.first()
    menus = FooterMenu.objects.prefetch_related("links").order_by("order")

    # Resolver hrefs de cada link
    for menu in menus:
        links = list(menu.links.all())
        try:
            links.sort(key=lambda link: (getattr(link, "order", 0), link.id))
        except Exception:
            pass

        for link in links:
            href = "#"

            named = getattr(link, "named_url", None)
            raw_kwargs = getattr(link, "named_url_kwargs", "")
            url_fallback = getattr(link, "url", None)

            if named:
                kwargs = _parse_kwargs(raw_kwargs)
                try:
                    href = reverse(named, kwargs=kwargs)
                except NoReverseMatch:
                    # Si el named_url no existe o faltan kwargs, usar URL si está
                    href = url_fallback or "#"
            elif url_fallback:
                href = url_fallback or "#"

            # propiedades derivadas para el template
            link.resolved_href = href
            link.target_attr = (
                "_blank" if getattr(link, "open_in_new_tab", False) else None
            )

        # lista con atributos extra (sin guion bajo: accesible en templates)
        menu.links_resolved = links

    # (Opcional) resolver href del bloque "about" si también tiene named/url
    if about:
        a_named = getattr(about, "named_url", None)
        a_kwargs_raw = getattr(about, "named_url_kwargs", "")
        a_url = getattr(about, "url", None)
        about.resolved_href = None
        if a_named:
            try:
                about.resolved_href = reverse(
                    a_named, kwargs=_parse_kwargs(a_kwargs_raw)
                )
            except NoReverseMatch:
                about.resolved_href = a_url or None
        elif a_url:
            about.resolved_href = a_url

    return {"about": about, "menus": menus}
