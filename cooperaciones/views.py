# cooperaciones/views.py
from django.shortcuts import render, get_object_or_404
from .models import CabeceraCoops, Cooperacion


def lista(request):
    cab = CabeceraCoops.objects.filter(publicado=True).first()
    coops = (
        Cooperacion.objects.filter(publicado=True)
        .select_related("categoria")
        .order_by("orden", "-creado")
    )
    return render(request, "cooperaciones/lista.html", {"cab": cab, "coops": coops})


def detalle(request, slug):
    coop = get_object_or_404(
        Cooperacion.objects.select_related("categoria").prefetch_related("fotos"),
        slug=slug,
        publicado=True,
    )
    if coop.categoria_id:
        relacionados = (
            Cooperacion.objects.filter(publicado=True, categoria=coop.categoria)
            .exclude(pk=coop.pk)
            .order_by("orden", "-creado")[:6]
        )
    else:
        relacionados = (
            Cooperacion.objects.filter(publicado=True)
            .exclude(pk=coop.pk)
            .order_by("orden", "-creado")[:6]
        )
    return render(
        request,
        "cooperaciones/detalle.html",
        {"coop": coop, "relacionados": relacionados},
    )
