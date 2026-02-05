# tienda/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import ProductoCategoria, Producto, ProductoImagen


@admin.register(ProductoCategoria)
class ProductoCategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "publicado", "orden")
    list_editable = ("publicado", "orden")
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("orden", "nombre")


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 0
    fields = ("publicado", "orden", "imagen", "alt", "mini")
    readonly_fields = ("mini",)
    ordering = ("orden",)

    def mini(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:6px">', obj.imagen.url
            )
        return "—"

    mini.short_description = "Preview"


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "mini",
        "titulo",
        "categoria",
        "precio",
        "precio_tachado",
        "publicado",
        "orden",
        "creado",
    )
    list_display_links = ("titulo",)  # hace clickeable el título
    list_editable = ("publicado", "orden")
    list_filter = ("publicado", "categoria")
    search_fields = ("titulo", "descripcion", "descripcion_corta", "slug")
    prepopulated_fields = {"slug": ("titulo",)}
    ordering = ("orden", "-creado")
    date_hierarchy = "creado"
    save_on_top = True
    list_select_related = ("categoria",)
    inlines = [ProductoImagenInline]

    actions = ["marcar_publicados", "marcar_no_publicados"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("categoria")

    def mini(self, obj):
        if obj.imagen_portada:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:6px">',
                obj.imagen_portada.url,
            )
        return "—"

    mini.short_description = " "

    def marcar_publicados(self, request, queryset):
        updated = queryset.update(publicado=True)
        self.message_user(request, f"{updated} producto(s) marcados como publicados.")

    marcar_publicados.short_description = "Publicar seleccionados"

    def marcar_no_publicados(self, request, queryset):
        updated = queryset.update(publicado=False)
        self.message_user(
            request, f"{updated} producto(s) marcados como NO publicados."
        )

    marcar_no_publicados.short_description = "Ocultar seleccionados"


# Admin “oculto” para acceder directo a /change/
class _Hidden(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(ProductoImagen)
class ProductoImagenAdmin(_Hidden):
    list_display = ("mini", "producto", "orden", "publicado")
    list_editable = ("orden", "publicado")
    ordering = ("producto", "orden")
    search_fields = ("producto__titulo", "alt")

    def mini(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:6px">', obj.imagen.url
            )
        return "—"

    mini.short_description = "Preview"
