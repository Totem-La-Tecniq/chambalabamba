# apps/visitas/admin.py
from django.contrib import admin
from .models import VisitsLanding, GuidedVisit, GuidedVisitPhoto


@admin.register(VisitsLanding)
class VisitsLandingAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Header", {"fields": ("publicado", "title", "background")}),
        ("Contenido", {"fields": ("intro_html", "sidebar_html", "instagram_embed")}),
    )


class GuidedVisitPhotoInline(admin.TabularInline):
    model = GuidedVisitPhoto
    extra = 1
    fields = ("publicado", "orden", "titulo", "imagen", "alt", "creditos", "is_header")
    ordering = ("orden",)


@admin.register(GuidedVisit)
class GuidedVisitAdmin(admin.ModelAdmin):
    list_display = ("orden", "titulo", "publicado", "fecha_inicio", "ubicacion")
    list_display_links = ("titulo",)  # <- el link es el TÍTULO
    list_editable = ("orden", "publicado")  # asegúrate de NO poner 'titulo' aquí
    ordering = ("orden", "-fecha_inicio")
    list_filter = ("publicado",)
    search_fields = ("titulo", "breve", "descripcion_html")
    prepopulated_fields = {"slug": ("titulo",)}
    inlines = [GuidedVisitPhotoInline]
    fieldsets = (
        ("Estado y orden", {"fields": ("publicado", "orden")}),
        ("Identificación", {"fields": ("titulo", "slug")}),
        ("Resumen/Descripción", {"fields": ("breve", "descripcion_html")}),
        (
            "Logística",
            {
                "fields": (
                    "ubicacion",
                    "punto_encuentro",
                    "duracion_minutos",
                    "cupo_maximo",
                    "fecha_inicio",
                    "fecha_fin",
                    "horario_text",
                    "frecuencia_text",
                )
            },
        ),
        (
            "Aportes y contacto",
            {
                "fields": (
                    "aporte_text",
                    "organizador",
                    "organizador_url",
                    "contacto_email",
                    "contacto_whatsapp",
                )
            },
        ),
        ("Imágenes", {"fields": ("portada", "inner_bg_override")}),
        (
            "SEO",
            {"classes": ("collapse",), "fields": ("meta_title", "meta_description")},
        ),
    )
