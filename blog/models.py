from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.conf import settings


def validate_local_or_url(value):
    """Permite http(s)://… o rutas internas que comiencen con /"""
    if not value:
        return
    if value.startswith("/"):
        return  # aceptamos rutas locales
    try:
        URLValidator(schemes=("http", "https"))(value)
    except ValidationError:
        raise ValidationError(
            "Ingrese una URL válida (http(s)://…) o una ruta interna que empiece con '/'."
        )


# ──────────────────────────────────────────────────────────────────────────────
# Base reutilizable
# ──────────────────────────────────────────────────────────────────────────────
class BaseOrdenPublicado(models.Model):
    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(default=timezone.now, null=True, blank=True)
    actualizado = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ("orden", "-creado")

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.creado:
            self.creado = now
        self.actualizado = now
        return super().save(*args, **kwargs)


# ──────────────────────────────────────────────────────────────────────────────
# Página & Header (inner header)
# ──────────────────────────────────────────────────────────────────────────────
class BlogHeader(models.Model):
    title = models.CharField(max_length=120, default="Blog")
    breadcrumb_label = models.CharField(max_length=120, default="Blog-Detail")
    background = models.ImageField(upload_to="blog/header/", blank=True, null=True)

    class Meta:
        verbose_name = "Blog · Inner Header"
        verbose_name_plural = "Blog · Inner Header"

    def __str__(self):
        return self.title


class BlogPage(models.Model):
    enabled = models.BooleanField(default=True)
    header = models.OneToOneField(
        BlogHeader, on_delete=models.SET_NULL, null=True, blank=True
    )

    # (opcional) textos generales
    intro_html = models.TextField(blank=True, default="")

    # Enlaces CTA del sidebar
    volunteer_url = models.URLField(blank=True, default="")
    donate_url = models.URLField(blank=True, default="")

    class Meta:
        verbose_name = "Página de Blog"
        verbose_name_plural = "Página de Blog"

    def __str__(self):
        return "Página del Blog"


# ──────────────────────────────────────────────────────────────────────────────
# Taxonomía y autoría
# ──────────────────────────────────────────────────────────────────────────────
class BlogAuthor(models.Model):
    nombre = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    foto = models.ImageField(upload_to="blog/autores/", blank=True, null=True)
    bio = models.TextField(blank=True, default="")

    def __str__(self):
        return self.nombre


class BlogCategory(models.Model):
    nombre = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class BlogTag(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.nombre


# ──────────────────────────────────────────────────────────────────────────────
# Post + Galería
# ──────────────────────────────────────────────────────────────────────────────
class BlogPost(BaseOrdenPublicado):
    TIPO = [
        ("standard", "Estándar"),
        ("gallery", "Galería"),
        ("video", "Video embebido"),
        ("audio", "Audio embebido"),
        ("link", "Enlace"),
    ]
    titulo = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    autor = models.ForeignKey(
        BlogAuthor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    categoria = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    tags = models.ManyToManyField(BlogTag, blank=True, related_name="posts")

    resumen = models.TextField(blank=True, default="")
    cuerpo_html = models.TextField(blank=True, default="")
    portada = models.ImageField(upload_to="blog/portadas/", blank=True, null=True)

    tipo = models.CharField(max_length=12, choices=TIPO, default="standard")
    video_url = models.URLField(blank=True, default="")
    audio_url = models.URLField(blank=True, default="")
    enlace_externo = models.URLField(blank=True, default="")

    fecha_publicacion = models.DateTimeField(default=timezone.now)
    comentarios_count = models.PositiveIntegerField(default=0)

    class Meta(BaseOrdenPublicado.Meta):
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.titulo

    @property
    def header_image(self):
        hdr = (
            self.fotos.filter(publicado=True, is_header=True)
            .order_by("orden", "id")
            .first()
        )
        if hdr and hdr.imagen:
            return hdr.imagen
        if self.portada:
            return self.portada
        first = self.fotos.filter(publicado=True).order_by("orden", "id").first()
        return first.imagen if first else None


class BlogPostPhoto(BaseOrdenPublicado):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="fotos")
    imagen = models.ImageField(upload_to="blog/gallery/")
    titulo = models.CharField(max_length=160, blank=True)
    alt = models.CharField(max_length=160, blank=True)
    creditos = models.CharField(max_length=160, blank=True)
    is_header = models.BooleanField(
        default=False, help_text="Usar como cabecera/slide principal"
    )

    class Meta:
        ordering = ("orden", "id")
        verbose_name = "Post · Foto"
        verbose_name_plural = "Post · Galería"
        constraints = [
            models.UniqueConstraint(
                fields=["post"],
                condition=models.Q(is_header=True),
                name="unique_header_photo_per_blogpost",
            )
        ]

    def __str__(self):
        return self.titulo or f"Foto {self.pk} · {self.post}"


# ──────────────────────────────────────────────────────────────────────────────
# Sidebar widgets
# ──────────────────────────────────────────────────────────────────────────────
class BlogSidebarWidget(BaseOrdenPublicado):
    TIPOS = [
        ("search", "Buscador"),
        ("text", "Texto"),
        ("latest_posts", "Últimos posts"),
        ("projects", "Proyectos actuales"),
        ("tags", "Tags"),
        ("recent_work", "Recent Work (carrusel)"),
        ("archives", "Archivos por mes"),
        ("cta_volunteer", "CTA Voluntariado"),
        ("cta_donate", "CTA Donaciones"),
        ("custom_html", "HTML libre"),
    ]
    page = models.ForeignKey(BlogPage, on_delete=models.CASCADE, related_name="widgets")
    tipo = models.CharField(max_length=20, choices=TIPOS)
    titulo = models.CharField(max_length=120, blank=True, default="")
    body_html = models.TextField(blank=True, default="")
    limite = models.PositiveIntegerField(default=5)

    # selección de proyectos (opcional) — se usa si existe app 'proyectos'
    proyectos = models.ManyToManyField(
        "proyectos.Project", blank=True, related_name="blog_widgets"
    )

    # enlaces CTA (usados según tipo)
    link_label = models.CharField(max_length=120, blank=True, default="")
    link_url = models.URLField(blank=True, default="")

    class Meta(BaseOrdenPublicado.Meta):
        verbose_name = "Sidebar · Widget"
        verbose_name_plural = "Sidebar · Widgets"

    def __str__(self):
        return f"{self.get_tipo_display()} · {self.titulo or 'sin título'}"


###############################comentarios###############################
class BlogComment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        APPROVED = "approved", "Aprobado"
        REJECTED = "rejected", "Rechazado"
        SPAM = "spam", "Spam"

    post = models.ForeignKey(
        "BlogPost", on_delete=models.CASCADE, related_name="comentarios"
    )
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    # Autoría (usuario autenticado opcional + campos públicos)
    user = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blog_comments",
    )
    nombre = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    cuerpo = models.TextField()

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    creado = models.DateTimeField(default=timezone.now, null=True, blank=True)
    actualizado = models.DateTimeField(default=timezone.now, null=True, blank=True)

    # Anti-spam / trazas (opcionales)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("creado", "id")
        indexes = [
            models.Index(fields=["post", "status", "creado"]),
        ]
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"

    def __str__(self):
        who = self.user or self.nombre or "Anónimo"
        return f"{who} → {self.post.titulo}"

    @property
    def visible(self):
        return self.status == self.Status.APPROVED
