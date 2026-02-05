# apps/donaciones/admin.py
from django.contrib import admin
from .models import DonacionSection, DonacionesStatic

"""
class DonacionMontoInline(admin.TabularInline):
    model = DonacionMonto
    extra = 0
    fields = ("etiqueta", "orden")
    ordering = ("orden",)
"""


@admin.register(DonacionSection)
class DonacionSectionAdmin(admin.ModelAdmin):
    list_display = ("slug", "titulo_superior", "titulo", "publicado", "orden")
    list_editable = ("publicado", "orden")
    search_fields = (
        "slug",
        "titulo",
        "descripcion",
        "intro_text",
        "success_title",
        "success_message",
        "canceled_title",
        "canceled_message",
        "paypal_redirect_message",
    )
    fields = (
        "slug",
        "titulo_superior",
        "titulo",
        "descripcion",
        "publicado",
        "orden",
    )


"""
@admin.register(Donacion)
class DonacionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "monto", "creado_en", "completado")
    list_filter = ("completado",)
    search_fields = ("nombre", "email", "paypal_id")
"""


@admin.register(DonacionesStatic)
class DonacionesStaticAdmin(admin.ModelAdmin):
    list_display = ("titulo",)
    fieldsets = (
        (None, {"fields": ("titulo", "contenido")}),
        (
            "Información de Contacto",
            {"fields": ("email_contacto", "telefono_contacto")},
        ),
        ("Media", {"fields": ("imagen",)}),
    )
