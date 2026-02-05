from django import template
from django.apps import apps
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.inclusion_tag("blog/_latest_posts_footer.html", takes_context=False)
def latest_posts_footer(limit=2):
    """
    Renderiza las últimas publicaciones para el footer.
    Devuelve 'footer_latest_posts' con [{'title','url','date','image'}, ...]
    """
    BlogPost = apps.get_model("blog", "BlogPost")
    posts = BlogPost.objects.filter(publicado=True).order_by("-fecha_publicacion")[
        :limit
    ]

    items = []
    for p in posts:
        # título flexible: usa 'titulo' o 'title' o str(p)
        title = getattr(p, "titulo", None) or getattr(p, "title", None) or str(p)

        # URL: get_absolute_url() o por slug con 'blog_detail'
        url = "#"
        if hasattr(p, "get_absolute_url"):
            try:
                url = p.get_absolute_url()
            except Exception:
                url = "#"
        else:
            slug = getattr(p, "slug", None)
            if slug:
                try:
                    url = reverse("blog_detail", kwargs={"slug": slug})
                except NoReverseMatch:
                    url = "#"

        # Imagen (opcional): prueba campos habituales
        image = None
        for fname in ("header_image", "portada", "imagen", "image"):
            f = getattr(p, fname, None)
            if f:
                try:
                    image = f.url
                    break
                except Exception:
                    pass

        items.append(
            {
                "title": title,
                "url": url,
                "date": getattr(p, "fecha_publicacion", None),
                "image": image,
            }
        )

    return {"footer_latest_posts": items}
