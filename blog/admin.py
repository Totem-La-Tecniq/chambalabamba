from django import forms
from django.utils.text import Truncator
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect
from .models import BlogComment

from .models import (
    BlogPage,
    BlogHeader,
    BlogAuthor,
    BlogCategory,
    BlogTag,
    BlogPost,
    BlogPostPhoto,
    BlogSidebarWidget,
)


# Helpers
class HiddenModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        if obj:
            return redirect(f"./{obj.pk}/change/")
        return super().changelist_view(request, extra_context)


# Inlines
class BlogPostPhotoInline(admin.TabularInline):
    model = BlogPostPhoto
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


class BlogSidebarWidgetInline(admin.StackedInline):
    model = BlogSidebarWidget
    extra = 0
    fields = (
        "publicado",
        "orden",
        "tipo",
        "titulo",
        "body_html",
        "limite",
        "proyectos",
        "link_label",
        "link_url",
    )
    autocomplete_fields = ("proyectos",)


# Filtro rápido: principales vs. respuestas
class ReplyTypeFilter(admin.SimpleListFilter):
    title = "tipo"
    parameter_name = "reply"

    def lookups(self, request, model_admin):
        return (("root", "Solo principales"), ("replies", "Solo respuestas"))

    def queryset(self, request, qs):
        if self.value() == "root":
            return qs.filter(parent__isnull=True)
        if self.value() == "replies":
            return qs.filter(parent__isnull=False)
        return qs


# Inline para ver/editar respuestas al abrir un comentario principal
class ReplyInline(admin.TabularInline):
    model = BlogComment
    fk_name = "parent"
    extra = 0
    fields = ("nombre", "email", "cuerpo", "status", "creado")
    readonly_fields = ("creado",)
    show_change_link = True


# Página
@admin.register(BlogPage)
class BlogPageAdmin(SingletonAdmin):
    readonly_fields = ("header_preview", "edit_header_link")
    fieldsets = (
        ("Estado", {"fields": ("enabled",)}),
        ("Header", {"fields": ("header", "header_preview", "edit_header_link")}),
        ("Intro (opcional)", {"fields": ("intro_html",)}),
        ("CTAs", {"fields": ("volunteer_url", "donate_url")}),
    )
    inlines = [BlogSidebarWidgetInline]
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
            url = reverse(
                f"admin:{hdr._meta.app_label}_{hdr._meta.model_name}_change",
                args=[hdr.pk],
            )
            return format_html(
                '<a class="button" href="{}" target="_blank">Editar header</a>', url
            )
        return "—"


# Header oculto del menú
try:
    admin.site.register(BlogHeader, HiddenModelAdmin)
except admin.sites.AlreadyRegistered:
    pass


# Taxonomía
@admin.register(BlogAuthor)
class BlogAuthorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    search_fields = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    search_fields = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    search_fields = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}


class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0
    fields = ("status", "nombre", "email", "cuerpo", "creado")
    readonly_fields = ("creado",)
    ordering = ("-creado",)


class BlogCommentAdminForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegura que se pueda dejar vacío y que se vea una opción vacía
        self.fields["parent"].required = False
        self.fields["parent"].empty_label = "— sin padre —"


@admin.action(description="Convertir a comentario principal (quitar padre)")
def clear_parent(modeladmin, request, queryset):
    queryset.update(parent=None)


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    form = BlogCommentAdminForm
    # columnas del listado
    list_display = (
        "short_body",  # preview del cuerpo (clickeable)
        "post",  # a qué post pertenece
        "author_label",  # nombre / usuario
        "parent_preview",  # si es respuesta, a quién
        "status",
        "creado",
    )
    list_display_links = ("short_body",)
    list_filter = ("status", ReplyTypeFilter, "creado", "post")
    search_fields = ("cuerpo", "nombre", "email", "post__titulo")
    ordering = ("-creado",)
    date_hierarchy = "creado"
    list_select_related = ("post", "parent", "user")
    autocomplete_fields = ("post", "user")
    raw_id_fields = ("parent",)  # <- esto te da la lupita + la ✖ Clear
    inlines = [ReplyInline]
    actions = [clear_parent]

    # --- helpers para columnas ---
    @admin.display(description="Mensaje")
    def short_body(self, obj: BlogComment):
        txt = obj.cuerpo or ""
        # corta a 80 chars y añade "…"
        return Truncator(txt).chars(80)

    @admin.display(description="Autor")
    def author_label(self, obj: BlogComment):
        if obj.nombre:
            return obj.nombre
        if obj.user_id:
            return obj.user.get_full_name() or obj.user.get_username()
        return "Anónimo"

    @admin.display(description="Responde a")
    def parent_preview(self, obj: BlogComment):
        if not obj.parent_id:
            return "—"
        p = obj.parent
        who = p.nombre or (
            p.user.get_full_name() or p.user.get_username() if p.user_id else "Anónimo"
        )
        prev = Truncator(p.cuerpo or "").chars(40)
        # flechita para que sea visualmente claro
        return format_html("↳ <strong>{}</strong>: {}", who, prev)


# Posts
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        "orden",
        "titulo",
        "categoria",
        "autor",
        "publicado",
        "fecha_publicacion",
        "comentarios_count",
    )
    list_display_links = ("titulo",)
    list_editable = ("orden", "publicado")
    list_filter = ("publicado", "categoria", "autor", "tipo")
    search_fields = ("titulo", "slug", "resumen", "cuerpo_html")
    prepopulated_fields = {"slug": ("titulo",)}
    inlines = [BlogPostPhotoInline]
    date_hierarchy = "fecha_publicacion"
    ordering = ("-fecha_publicacion", "orden", "titulo")
    inlines = [BlogPostPhotoInline, BlogCommentInline]
