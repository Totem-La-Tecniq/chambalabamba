# participa/admin.py
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from .models import (
    VoluntariadoPage,
    ContentBlock,  # ya lo usas en Voluntariado
    EstanciasIntro,  # singleton de la sección
)
from .models import ProyectoVoluntariado

from .models import (
    ParticipaPage,
    ParticipaHeader,
    Estancia,
    EstanciaFoto,
    EstanciaSpec,
    InstaGallery,
    InstaItem,  # si no los usas aún, quedan ocultos
)
from django.contrib.admin.sites import AlreadyRegistered


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        if obj:
            from django.shortcuts import redirect

            return redirect(f"./{obj.pk}/change/")
        return super().changelist_view(request, extra_context)


# 🔒 Ocultar del sidebar pero mantener búsqueda para el autocompletado
class HiddenModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}  # sin permisos -> no aparece en el índice

    # opcional: también bloquear “Add” directo por URL
    def has_add_permission(self, request):
        return False

    # necesario para que autocomplete_fields funcione bien
    search_fields = ("title", "body_html")


@admin.register(ContentBlock)
class ContentBlockAdmin(HiddenModelAdmin):
    pass


@admin.register(VoluntariadoPage)
class VoluntariadoPageAdmin(SingletonAdmin):
    autocomplete_fields = ("about_block", "ambiente_block")
    readonly_fields = ("edit_about_link", "edit_ambiente_link")
    fieldsets = (
        ("Estado", {"fields": ("publicado",)}),
        ("Cabecera", {"fields": ("titulo", "subtitulo", "background", "thumb")}),
        (
            "Bloques",
            {
                "fields": (
                    "about_block",
                    "edit_about_link",
                    "ambiente_block",
                    "edit_ambiente_link",
                )
            },
        ),
        ("Texto de introducción (fallback)", {"fields": ("intro_html",)}),
        ("Quote", {"fields": ("quote_text", "quote_author")}),
        ("Instagram", {"fields": ("instagram_embed_url",)}),
        ("Contacto", {"fields": ("contact_cta_label", "contact_cta_url")}),
    )
    # … (deja tus helpers edit_about_link / edit_ambiente_link iguales)

    # ---------------- helpers de enlace directo ----------------
    def edit_about_link(self, obj):
        if obj and obj.about_block_id:
            url = reverse(
                "admin:participa_contentblock_change", args=[obj.about_block_id]
            )
            return format_html(
                '<a class="button" href="{}" target="_blank">Editar “{}”</a>',
                url,
                obj.about_block,
            )
        return "—"

    edit_about_link.short_description = "Editar About"

    def edit_ambiente_link(self, obj):
        if obj and obj.ambiente_block_id:
            url = reverse(
                "admin:participa_contentblock_change", args=[obj.ambiente_block_id]
            )
            return format_html(
                '<a class="button" href="{}" target="_blank">Editar “{}”</a>',
                url,
                obj.ambiente_block,
            )
        return "—"

    edit_ambiente_link.short_description = "Editar Ambiente"


# apps/estancias/admin.py


class EstanciasIntroInline(admin.StackedInline):
    model = EstanciasIntro
    can_delete = False
    extra = 0
    fieldsets = (
        (None, {"fields": ("publicado", "title", "body_html", "quote_text")}),
        ("Estilo", {"fields": ("bg_color", "margin_top_px")}),
    )


# ──────────────────────────────────────────────────────────────────────────────
# Utilidades
# ──────────────────────────────────────────────────────────────────────────────
class HiddenModelAdmin(admin.ModelAdmin):
    """No aparece en el índice del admin."""

    def get_model_perms(self, request):
        return {}

    # útil si los usas vía autocomplete
    search_fields = ("id",)


class SingletonAdmin(admin.ModelAdmin):
    """Redirige el changelist al único registro y evita múltiples 'add'."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        if obj:
            return redirect(f"./{obj.pk}/change/")
        return super().changelist_view(request, extra_context)


# ──────────────────────────────────────────────────────────────────────────────
# Inlines
# ──────────────────────────────────────────────────────────────────────────────
class EstanciaFotoInline(admin.TabularInline):
    model = EstanciaFoto
    extra = 1
    fields = ("publicado", "orden", "imagen", "preview", "titulo", "alt")
    readonly_fields = ("preview",)
    ordering = ("orden", "id")

    def preview(self, obj):
        if getattr(obj, "imagen", None):
            return format_html(
                '<img src="{}" style="height:60px; border-radius:4px;" />',
                obj.imagen.url,
            )
        return "—"


class EstanciaSpecInline(admin.TabularInline):
    model = EstanciaSpec
    extra = 0
    fields = ("orden", "clave", "valor")
    ordering = ("orden", "id")


# ──────────────────────────────────────────────────────────────────────────────
# Estancia (listado principal)
# ──────────────────────────────────────────────────────────────────────────────


class HiddenModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


try:
    admin.site.register(ParticipaHeader, HiddenModelAdmin)
except AlreadyRegistered:
    pass


@admin.register(Estancia)
class EstanciaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo", "precio", "publicado", "orden")
    list_editable = ("publicado", "orden")
    search_fields = ("titulo", "slug", "resumen", "descripcion", "tipo", "lugar")
    list_filter = ("seccion", "publicado")
    prepopulated_fields = {"slug": ("titulo",)}
    readonly_fields = ("portada_preview",)
    fieldsets = (
        ("Estado", {"fields": ("publicado", "orden", "seccion")}),
        ("Datos", {"fields": ("titulo", "slug", "tipo", "lugar")}),
        ("Portada", {"fields": ("portada", "portada_preview", "alt_portada")}),
        ("Textos", {"fields": ("resumen", "descripcion")}),
        ("Precio", {"fields": ("precio", "precio_tachado")}),
        ("Contacto", {"fields": ("phone_whatsapp",)}),
    )
    inlines = [EstanciaFotoInline, EstanciaSpecInline]

    actions = ["publicar", "despublicar"]

    def portada_preview(self, obj):
        # usa tu campo 'portada' de Estancia
        if getattr(obj, "portada", None):
            return format_html(
                '<img src="{}" style="height:80px; border-radius:6px;" />',
                obj.portada.url,
            )
        return "—"

    portada_preview.short_description = "Preview portada"

    def publicar(self, request, queryset):
        queryset.update(publicado=True)

    publicar.short_description = "Marcar como publicados"

    def despublicar(self, request, queryset):
        queryset.update(publicado=False)

    despublicar.short_description = "Marcar como NO publicados"


# ──────────────────────────────────────────────────────────────────────────────
# Página Participa (singleton con preview del header)
# ──────────────────────────────────────────────────────────────────────────────
@admin.register(ParticipaPage)
class ParticipaPageAdmin(SingletonAdmin):
    readonly_fields = ("header_preview", "edit_header_link")
    fieldsets = (
        ("Estado", {"fields": ("enabled",)}),
        ("Header", {"fields": ("header", "header_preview", "edit_header_link")}),
    )
    list_display = ("id", "enabled", "header")

    def header_preview(self, obj):
        hdr = obj.header
        if hdr and getattr(hdr, "background", None):
            return format_html(
                '<img src="{}" style="height:80px;border-radius:6px;" />',
                hdr.background.url,
            )
        return "—"

    header_preview.short_description = "Preview fondo"

    def edit_header_link(self, obj):
        hdr = getattr(obj, "header", None)
        if hdr and hdr.pk:
            # nombre del admin construido desde los metadatos del modelo
            url_name = f"admin:{hdr._meta.app_label}_{hdr._meta.model_name}_change"
            try:
                url = reverse(url_name, args=[hdr.pk])
                return format_html(
                    '<a class="button" href="{}" target="_blank">Editar header</a>', url
                )
            except Exception:
                # Evita que el admin casque si por algo no está registrado
                return format_html(
                    '<span style="color:#999">URL no disponible ({})</span>', url_name
                )
        return "—"

    inlines = [EstanciasIntroInline]


# Ocultar del sidebar: Header + modelos “base”
try:
    admin.site.register(ParticipaHeader, HiddenModelAdmin)
except admin.sites.AlreadyRegistered:
    pass

# (Opcional) también ocultar InstaGallery/Item si aún no los expones
for mdl in (InstaGallery, InstaItem):
    try:
        admin.site.register(mdl, HiddenModelAdmin)
    except admin.sites.AlreadyRegistered:
        pass


# *************************PROYECTOS DE VOLUNTARIADO*****************************#
@admin.register(ProyectoVoluntariado)
class ProyectoVoluntariadoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "publicado", "orden")
    list_editable = ("publicado", "orden")
    search_fields = ("nombre", "descripcion", "slug")
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("orden", "nombre")
