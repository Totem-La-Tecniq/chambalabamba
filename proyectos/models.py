# proyectos/models.py
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# ── Base con orden/publicado (como antes) ─────────────────────────────────────
class BaseOrdenPublicado(models.Model):
    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("orden", "-creado")


# ── Catálogo de proyectos ─────────────────────────────────────────────────────
class Project(BaseOrdenPublicado):
    ESTADO = [
        ("current", "Actual"),
        ("paused", "Pausado"),
        ("done", "Finalizado"),
    ]
    titulo = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    resumen = models.TextField(blank=True)
    body_html = models.TextField(blank=True)

    # Imagen “principal” opcional (fallback si no hay foto marcada como header)
    imagen = models.ImageField(upload_to="proyectos/", blank=True, null=True)
    url = models.URLField(blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO, default="current")
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.titulo

    # Helper para obtener la imagen de cabecera (portada) de forma consistente
    @property
    def header_image(self):
        # 1) alguna foto de la galería marcada como cabecera
        header = (
            self.fotos.filter(publicado=True, is_header=True)
            .order_by("orden", "id")
            .first()
        )
        if header and header.imagen:
            return header.imagen
        # 2) el campo 'imagen' del propio proyecto
        if self.imagen:
            return self.imagen
        # 3) primera foto publicada de la galería
        first = self.fotos.filter(publicado=True).order_by("orden", "id").first()
        return first.imagen if first else None


# ── Galería del proyecto ──────────────────────────────────────────────────────
class ProjectPhoto(BaseOrdenPublicado):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="fotos")
    imagen = models.ImageField(upload_to="proyectos/gallery/")
    titulo = models.CharField(max_length=160, blank=True)
    alt = models.CharField(max_length=160, blank=True)
    creditos = models.CharField(max_length=160, blank=True)
    is_header = models.BooleanField(
        default=False, help_text="Usar como cabecera/portada"
    )

    class Meta:
        ordering = ("orden", "id")
        verbose_name = "Proyecto · Foto"
        verbose_name_plural = "Proyecto · Galería"
        # Asegura solo una foto marcada como cabecera por proyecto (opcional pero recomendable)
        constraints = [
            models.UniqueConstraint(
                fields=["project"],
                condition=models.Q(is_header=True),
                name="unique_header_per_project",
            )
        ]

    def __str__(self):
        return self.titulo or f"Foto {self.pk} · {self.project}"


# ── Placement genérico (para pegar proyectos en cualquier página) ─────────────
class ProjectPlacement(BaseOrdenPublicado):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="placements"
    )
    titulo_bloque = models.CharField(
        max_length=160, blank=True, default="Proyectos actuales"
    )
    nota = models.TextField(blank=True)

    class Meta:
        verbose_name = "Colocación de proyecto"
        verbose_name_plural = "Colocaciones de proyectos"

    def __str__(self):
        return f"{self.project} → {self.content_type.app_label}.{self.content_type.model} #{self.object_id}"


# Create your models here.
