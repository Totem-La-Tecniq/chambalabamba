from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from .models import HeroSlide, ValorCard
from .models import Gallery, GalleryItem, SectionHeader


class BaseOrdenPublicadoAdmin(admin.ModelAdmin):
    list_editable = ("publicado", "orden")
    list_filter = ("publicado",)
    ordering = ("orden",)
    search_fields = ("titulo",)


@admin.register(HeroSlide)
class HeroSlideAdmin(BaseOrdenPublicadoAdmin):
    list_display = ("mini", "titulo", "subtitulo", "publicado", "orden", "creado")

    def mini(self, obj):
        return (
            format_html(
                '<img src="{}" style="height:40px;border-radius:6px">', obj.imagen.url
            )
            if obj.imagen
            else "—"
        )


@admin.register(ValorCard)
class ValorCardAdmin(BaseOrdenPublicadoAdmin):
    list_display = (
        "mini",
        "titulo",
        "descripcion",
        "link_url",
        "publicado",
        "orden",
        "creado",
    )

    def mini(self, obj):
        return (
            format_html('<img src="{}" style="height:28px">', obj.icono.url)
            if obj.icono
            else "—"
        )


# GALERIA INICIAL ULTIMOS EVENTOS


class GalleryItemInline(admin.TabularInline):
    model = GalleryItem
    extra = 1
    fields = ("publicado", "orden", "titulo", "imagen", "alt", "credito", "tags")
    ordering = ("orden",)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("titulo", "seccion", "publicado", "orden", "creado")
    list_filter = ("seccion", "publicado")
    search_fields = ("titulo", "slug", "descripcion_breve", "descripcion")
    prepopulated_fields = {"slug": ("titulo",)}
    inlines = [GalleryItemInline]

    # Orden y agrupación del formulario:
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "publicado",
                    "orden",
                    "titulo",
                    "slug",
                    "seccion",
                    "descripcion_breve",  # NUEVO (para portada)
                    "descripcion",  # LARGA (para la vista detalle)
                    "portada",
                    "alt_portada",
                )
            },
        ),
    )


@admin.register(SectionHeader)
class SectionHeaderAdmin(admin.ModelAdmin):
    list_display = ("seccion", "title", "subtitle", "limit", "publicado")
    list_editable = ("publicado",)
    search_fields = ("seccion", "title", "subtitle")
