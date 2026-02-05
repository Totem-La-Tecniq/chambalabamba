from django.contrib import admin
from django.utils.html import format_html
from .models import (
    NosotrosPage,
    InnerHeader,
    AboutSection,
    HistorySection,
    TimelinePeriod,
    TimelineItem,
    EcoAldeaSection,
    EcoAldeaCard,
    PilarPage,
    PilarParagraph,
    PilarQuote,
    PilarSidebarWidget,
)

from django.urls import reverse
from django.shortcuts import redirect

from .models import TopicPage


from .models import (
    TopicParagraph,
    TopicQuote,
    TopicSidebarWidget,
    GobernanzaPage,
    PrincipiosValoresPage,
    TerritorioPage,
)


# --- Utilidades ---
class HiddenModelAdmin(admin.ModelAdmin):
    """No aparece en el índice, pero mantiene funcionalidades al entrar por URL."""

    def get_model_perms(self, request):
        return {}


class SingletonAdmin(admin.ModelAdmin):
    """Redirige el changelist al único registro y evita múltiples 'add'."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        if obj:
            return redirect(f"./{obj.pk}/change/")
        return super().changelist_view(request, extra_context)


# --- Inlines que ya tenías (timeline y ecoaldea) ---
class TimelineItemInline(admin.TabularInline):
    model = TimelineItem
    extra = 1
    fields = ("order", "title", "body")
    ordering = ("order",)


class TimelinePeriodInline(admin.StackedInline):
    model = TimelinePeriod
    extra = 0
    show_change_link = True


class EcoAldeaCardInline(admin.TabularInline):
    model = EcoAldeaCard
    extra = 0
    fields = ("order", "icon", "title", "text", "link_text", "link_url")
    ordering = ("order",)


# --- Admin “ocultos” para secciones, conservando sus inlines ---
@admin.register(InnerHeader)
class InnerHeaderAdmin(HiddenModelAdmin):
    list_display = ("title", "breadcrumb_label")
    search_fields = ("title", "breadcrumb_label")


@admin.register(AboutSection)
class AboutSectionAdmin(HiddenModelAdmin):
    list_display = ("title", "cta_text", "video_url")
    search_fields = ("title", "cta_text", "video_url")


@admin.register(HistorySection)
class HistorySectionAdmin(HiddenModelAdmin):
    list_display = ("title", "subtitle")
    inlines = [TimelinePeriodInline]
    search_fields = ("title", "subtitle")


@admin.register(TimelinePeriod)
class TimelinePeriodAdmin(HiddenModelAdmin):
    inlines = [TimelineItemInline]
    list_display = ("label", "history", "order")
    list_filter = ("history",)
    ordering = ("history", "order")
    search_fields = ("label",)


@admin.register(EcoAldeaSection)
class EcoAldeaSectionAdmin(HiddenModelAdmin):
    list_display = ("title",)
    inlines = [EcoAldeaCardInline]
    search_fields = ("title",)


# --- Página centralizada (única entrada visible) ---
@admin.register(NosotrosPage)
class NosotrosPageAdmin(SingletonAdmin):
    readonly_fields = (
        "header_preview",
        "edit_header_link",
        "edit_about_link",
        "edit_history_link",
        "edit_ecoaldea_link",
    )
    fieldsets = (
        ("Estado", {"fields": ("enabled",)}),
        (
            "1) Cabecera (InnerHeader)",
            {
                "description": "Imagen de fondo, título y breadcrumb actual.",
                "fields": ("header", "header_preview", "edit_header_link"),
            },
        ),
        (
            "2) Acerca + Video",
            {
                "description": "Bloque de introducción, botón/URL y video.",
                "fields": ("about", "edit_about_link"),
            },
        ),
        (
            "3) Historia (timeline)",
            {
                "description": "Incluye periodos y cajas del timeline (edítalas en la sección con inlines).",
                "fields": ("history", "edit_history_link"),
            },
        ),
        (
            "4) EcoAldea (tarjetas)",
            {
                "description": "Tres tarjetas con icono, texto y link.",
                "fields": ("ecoaldea", "edit_ecoaldea_link"),
            },
        ),
    )
    list_display = ("id", "enabled", "header", "about", "history", "ecoaldea")
    save_on_top = True

    # --- Previews / Links ---
    def header_preview(self, obj):
        hdr = obj.header
        if hdr and getattr(hdr, "background", None):
            return format_html(
                '<img src="{}" style="height:80px;border-radius:6px;" />',
                hdr.background.url,
            )
        return "—"

    header_preview.short_description = "Preview fondo"

    def _edit_link(self, obj, rel_attr, change_url_name, add_url_name, label):
        sec = getattr(obj, rel_attr)
        if sec:
            url = reverse(change_url_name, args=[sec.pk])
            return format_html('<a class="button" href="{}">Editar {}</a>', url, label)
        else:
            url = reverse(add_url_name)
            return format_html('<a class="button" href="{}">Crear {}</a>', url, label)

    def edit_header_link(self, obj):
        return self._edit_link(
            obj,
            "header",
            "admin:nosotros_innerheader_change",
            "admin:nosotros_innerheader_add",
            "Cabecera",
        )

    def edit_about_link(self, obj):
        return self._edit_link(
            obj,
            "about",
            "admin:nosotros_aboutsection_change",
            "admin:nosotros_aboutsection_add",
            "About",
        )

    def edit_history_link(self, obj):
        return self._edit_link(
            obj,
            "history",
            "admin:nosotros_historysection_change",
            "admin:nosotros_historysection_add",
            "Historia",
        )

    def edit_ecoaldea_link(self, obj):
        return self._edit_link(
            obj,
            "ecoaldea",
            "admin:nosotros_ecoaldeasection_change",
            "admin:nosotros_ecoaldeasection_add",
            "EcoAldea",
        )

    # --- Bootstrap automático de secciones faltantes al guardar ---
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        created = False
        if obj.header is None:
            obj.header = InnerHeader.objects.create()
            created = True
        if obj.about is None:
            obj.about = AboutSection.objects.create()
            created = True
        if obj.history is None:
            obj.history = HistorySection.objects.create()
            created = True
        if obj.ecoaldea is None:
            obj.ecoaldea = EcoAldeaSection.objects.create()
            created = True
        if created:
            obj.save()


# ======= (El resto de tu admin de Pilares y Secciones temáticas puede quedarse igual) =======
# Si quieres, también puedes ocultar TopicPage / PilarPage del índice aplicando HiddenModelAdmin con sus inlines.


# =========================
# P I L A R E S
# =========================
class NoAddButtonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False  # oculta el "+ Add" del sidebar y el botón "Add" del changelist


class PilarParagraphInline(admin.TabularInline):
    model = PilarParagraph
    extra = 0
    fields = ("orden", "publicado", "body")
    ordering = ("orden",)  # usa ("orden", "-creado") si el modelo tiene 'creado'


class PilarQuoteInline(admin.TabularInline):
    model = PilarQuote
    extra = 0
    fields = ("orden", "publicado", "text")
    ordering = ("orden",)  # idem


class PilarSidebarInline(admin.TabularInline):
    model = PilarSidebarWidget
    extra = 0
    fields = ("orden", "publicado", "title", "text")
    ordering = ("orden",)  # idem


@admin.register(PilarPage)
class PilarPageAdmin(NoAddButtonAdmin):
    list_display = (
        "slug",
        "title",
    )
    list_filter = ("slug",)
    search_fields = ("title",)
    inlines = [PilarParagraphInline, PilarQuoteInline, PilarSidebarInline]
    save_on_top = True
    list_per_page = 20


# ──────────────────────────────────────────────────────────────────────────────
# NOSOTROS: Secciones (Gobernanza, Principios y valores, Territorio)
# ──────────────────────────────────────────────────────────────────────────────


class TopicParagraphInline(admin.TabularInline):
    model = TopicParagraph
    extra = 0
    fields = ("orden", "publicado", "body")
    ordering = ("orden",)


class TopicQuoteInline(admin.TabularInline):
    model = TopicQuote
    extra = 0
    fields = ("orden", "publicado", "text")
    ordering = ("orden",)


class TopicSidebarInline(admin.TabularInline):
    model = TopicSidebarWidget
    extra = 0
    fields = ("orden", "publicado", "title", "text")
    ordering = ("orden",)


@admin.register(TopicPage)
class TopicPageAdmin(admin.ModelAdmin):
    list_display = ("slug", "title")
    list_filter = ("slug",)
    search_fields = ("title",)
    inlines = [TopicParagraphInline, TopicQuoteInline, TopicSidebarInline]
    save_on_top = True


# nosotros/admin.py
class ParagraphInline(admin.StackedInline):
    model = TopicParagraph
    extra = 0


class QuoteInline(admin.StackedInline):
    model = TopicQuote
    extra = 0


class SidebarInline(admin.StackedInline):
    model = TopicSidebarWidget
    extra = 0


class _BaseTopicAdmin(admin.ModelAdmin):
    inlines = [ParagraphInline, QuoteInline, SidebarInline]
    fields = ("title", "header", "slug")  # o los campos que edites
    readonly_fields = ("slug",)  # fijamos slug

    # Evita que creen más de 1 registro por proxy
    def has_add_permission(self, request):
        return self.get_queryset(request).count() == 0

    # Oculta cualquier otro registro que no sea el de este slug
    filter_slug = None  # lo define cada subclase

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(slug=self.filter_slug)

    # Si quisieras autocrear el registro al entrar por 1a vez:
    def changelist_view(self, request, extra_context=None):
        if self.model.objects.filter(slug=self.filter_slug).count() == 0:
            self.model.objects.create(
                slug=self.filter_slug,
                title=self.model._meta.verbose_name.split(". ", 1)[1],
            )
        return super().changelist_view(request, extra_context)


@admin.register(GobernanzaPage)
class GobernanzaAdmin(_BaseTopicAdmin):
    filter_slug = "gobernanza"


@admin.register(PrincipiosValoresPage)
class PrincipiosValoresAdmin(_BaseTopicAdmin):
    filter_slug = "principios-y-valores"


@admin.register(TerritorioPage)
class TerritorioAdmin(_BaseTopicAdmin):
    filter_slug = "territorio"


# Oculta el modelo base del índice del admin
try:
    admin.site.unregister(TopicPage)
except admin.sites.NotRegistered:
    pass
