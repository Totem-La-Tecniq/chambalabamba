# apps/contenido/admin.py
from django.contrib import admin
from .models import MediaAsset, Gallery, GalleryItem, Placement
from .models import FooterSettings, FooterMenu, FooterLink


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("titulo", "creado")
    search_fields = ("titulo", "tags")


class GalleryItemInline(admin.TabularInline):
    model = GalleryItem
    extra = 1


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("titulo", "slug", "publicado", "creado")
    list_filter = ("publicado",)
    search_fields = ("titulo",)
    inlines = [GalleryItemInline]


# @admin.register(Flyer)
class FlyerAdmin(admin.ModelAdmin):
    list_display = ("titulo", "ratio", "publicado", "creado")
    list_filter = ("publicado", "ratio")
    search_fields = ("titulo",)


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ("key", "flyer", "gallery", "activo")
    list_filter = ("activo",)
    search_fields = ("key",)


@admin.register(FooterSettings)
class FooterSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Contenido", {"fields": ("title", "text")}),
        (
            "Enlace",
            {
                "fields": (
                    "link_label",
                    "named_url",
                    "named_url_kwargs",
                    "url",
                    "open_in_new_tab",
                )
            },
        ),
    )


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    fields = (
        "order",
        "label",
        "named_url",
        "named_url_kwargs",
        "url",
        "open_in_new_tab",
    )


@admin.register(FooterMenu)
class FooterMenuAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    ordering = ("order", "id")
    inlines = [FooterLinkInline]
