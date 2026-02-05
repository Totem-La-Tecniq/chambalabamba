from django.db import models

# Create your models here.
# apps/visitas/models.py
from django.utils.text import slugify


class VisitsLanding(models.Model):
    publicado = models.BooleanField(default=True)
    # Inner header
    title = models.CharField(
        "Título de la página", max_length=120, default="Visitas guiadas"
    )
    background = models.ImageField(
        "Imagen de cabecera (inner header)",
        upload_to="visitas/landing/",
        blank=True,
        null=True,
    )
    # Contenidos
    intro_html = models.TextField(blank=True, help_text="Cuerpo principal en HTML.")
    intro_image = models.ImageField(upload_to="visitas/landing/", blank=True, null=True)
    sidebar_html = models.TextField(blank=True, help_text="Sidebar en HTML.")
    instagram_embed = models.URLField(
        blank=True, help_text="URL a reel/post (opcional)."
    )

    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "1) Página de Visitas guiadas (landing)"
        verbose_name_plural = "1) Página de Visitas guiadas (landing)"

    def __str__(self):
        return "Página: Visitas guiadas"


class GuidedVisit(models.Model):
    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    titulo = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)

    breve = models.CharField(max_length=200, blank=True)
    descripcion_html = models.TextField(blank=True)

    # Logística
    ubicacion = models.CharField(max_length=140, blank=True)
    punto_encuentro = models.CharField(max_length=140, blank=True)
    duracion_minutos = models.PositiveIntegerField(default=60)
    cupo_maximo = models.PositiveIntegerField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    horario_text = models.CharField(max_length=120, blank=True)
    frecuencia_text = models.CharField(max_length=120, blank=True)

    # Aportes/organización
    aporte_text = models.CharField(max_length=120, blank=True)
    organizador = models.CharField(max_length=120, blank=True)
    organizador_url = models.URLField(blank=True)
    contacto_email = models.EmailField(blank=True)
    contacto_whatsapp = models.CharField(max_length=40, blank=True)

    # Imágenes
    portada = models.ImageField(
        upload_to="visitas/portadas/",
        blank=True,
        null=True,
        help_text="Imagen destacada para grillas/listados.",
    )
    inner_bg_override = models.ImageField(
        upload_to="visitas/inner/",
        blank=True,
        null=True,
        help_text="Opcional: reemplaza el fondo del inner-header en el detalle.",
    )

    # SEO opcional
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=200, blank=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("orden", "titulo")
        verbose_name = "2) Galeria visita guiada"
        verbose_name_plural = "2) Galeria visitas guiadas"

    def __str__(self):
        return self.titulo

    def save(self, *a, **kw):
        if not self.slug:
            self.slug = slugify(self.titulo)[:50]
        return super().save(*a, **kw)

    def get_absolute_url(self):
        return f"/visitas/{self.slug}/"


class GuidedVisitPhoto(models.Model):
    visita = models.ForeignKey(
        GuidedVisit, on_delete=models.CASCADE, related_name="fotos"
    )
    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    titulo = models.CharField(max_length=140, blank=True)
    imagen = models.ImageField(upload_to="visitas/galeria/")
    alt = models.CharField(max_length=200, blank=True)
    creditos = models.CharField(max_length=140, blank=True)
    is_header = models.BooleanField(
        default=True, help_text="Incluye en slider/galería de cabecera del detalle."
    )

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("visita", "orden")
        verbose_name = "2.1) Foto de visita guiada"
        verbose_name_plural = "2.1) Fotos de visita guiada"

    def __str__(self):
        return f"{self.visita} · {self.titulo or self.imagen.name}"
