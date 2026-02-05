# proyectos/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Project, ProjectPhoto, ProjectPlacement


class ProjectPhotoInline(admin.TabularInline):
    model = ProjectPhoto
    extra = 1
    fields = (
        "publicado",
        "orden",
        "imagen",
        "preview",
        "titulo",
        "alt",
        "creditos",
        "is_header",
    )
    readonly_fields = ("preview",)
    ordering = ("orden", "id")

    def preview(self, obj):
        if getattr(obj, "imagen", None):
            return format_html(
                '<img src="{}" style="height:60px;border-radius:4px;" />',
                obj.imagen.url,
            )
        return "—"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("titulo", "estado", "publicado", "orden")
    list_display_links = ("titulo",)
    list_editable = ("publicado", "orden")
    list_filter = ("estado", "publicado")
    search_fields = ("titulo", "slug", "resumen", "body_html")
    prepopulated_fields = {"slug": ("titulo",)}
    inlines = [ProjectPhotoInline]
    ordering = ("estado", "orden", "titulo")


@admin.register(ProjectPlacement)
class ProjectPlacementAdmin(admin.ModelAdmin):
    list_display = ("project", "publicado", "orden", "content_type", "object_id")
    list_editable = ("publicado", "orden")
    list_filter = ("publicado", "content_type")
    autocomplete_fields = ("project",)
    search_fields = ("project__titulo", "nota")
    ordering = ("content_type", "object_id", "orden")
