from django.contrib import admin
from django.utils.html import format_html
from .models import CabeceraCoops, CoopCategoria, Cooperacion, CoopFoto


@admin.register(CabeceraCoops)
class CabeceraAdmin(admin.ModelAdmin):
    list_display = ("h5", "h2", "publicado", "actualizado")
    list_editable = ("publicado",)


@admin.register(CoopCategoria)
class CoopCategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "publicado", "orden")
    list_editable = ("publicado", "orden")
    prepopulated_fields = {"slug": ("nombre",)}
    search_fields = ("nombre",)


class CoopFotoInline(admin.TabularInline):
    model = CoopFoto
    extra = 0
    fields = ("publicado", "orden", "imagen", "alt", "mini")
    readonly_fields = ("mini",)
    ordering = ("orden",)

    def mini(self, obj):
        return (
            format_html(
                '<img src="{}" style="height:40px;border-radius:6px">', obj.imagen.url
            )
            if obj.imagen
            else "—"
        )


@admin.register(Cooperacion)
class CooperacionAdmin(admin.ModelAdmin):
    list_display = (
        "mini",
        "nombre",
        "categoria",
        "pais",
        "publicado",
        "orden",
        "creado",
    )
    list_editable = ("publicado", "orden")
    list_filter = ("publicado", "categoria", "pais")
    search_fields = ("nombre", "slug", "descripcion", "excerpt")
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("orden", "-creado")
    inlines = [CoopFotoInline]

    def mini(self, obj):
        img = obj.logo or obj.portada
        return (
            format_html('<img src="{}" style="height:40px;border-radius:6px">', img.url)
            if img
            else "—"
        )


@admin.register(CoopFoto)
class CoopFotoAdmin(admin.ModelAdmin):
    list_display = ("coop", "orden", "publicado")
    list_editable = ("orden", "publicado")
