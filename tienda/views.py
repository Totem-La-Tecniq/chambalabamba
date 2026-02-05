from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Producto, TiendaLanding

# ⚠️ Ajusta este import según tu app real:
# p.ej. from inicio.models import Gallery  ó  from galeria.models import Gallery
from inicio.models import Gallery


def lista_productos(request):
    landing = TiendaLanding.objects.filter(publicado=True).first()

    qs = (
        Producto.objects.filter(publicado=True)
        .select_related("categoria")
        .prefetch_related("imagenes")
        .order_by("orden", "-creado")
    )

    cat = request.GET.get("cat")
    if cat:  # slug de categoría
        qs = qs.filter(categoria__slug=cat)

    q = request.GET.get("q")
    if q:
        # Mejor con Q para OR:
        qs = qs.filter(Q(titulo__icontains=q) | Q(descripcion__icontains=q))

    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "tienda/panel-productos.html",
        {
            "productos": page_obj.object_list,
            "page_obj": page_obj,
            "q": q,
            "cat": cat,
            "tienda_landing": landing,
        },
    )


def detalle_producto(request, slug):
    producto = get_object_or_404(
        Producto.objects.select_related("categoria").prefetch_related("imagenes"),
        slug=slug,
        publicado=True,
    )
    relacionados = (
        Producto.objects.filter(publicado=True, categoria=producto.categoria)
        .exclude(pk=producto.pk)
        .order_by("orden")[:4]
    )
    return render(
        request,
        "tienda/detalle-producto.html",
        {"producto": producto, "relacionados": relacionados},
    )


def productos_home(request):
    productos = (
        Producto.objects.filter(publicado=True)
        .prefetch_related("imagenes")
        .order_by("orden", "-creado")[:12]
    )

    galerias = (
        Gallery.objects.filter(seccion="tienda_home", publicado=True)
        .exclude(portada="")
        .order_by("orden", "-creado")[:8]
    )

    return render(
        request,
        "tienda/productos_home.html",
        {
            "productos": productos,
            "galerias": galerias,  # <- para el slider
            "title": "Visita nuestra sección de productos",
            "subtitle": "Proyectos en movimiento",
            "usar_imagen_relacionada": True,
        },
    )
