from django.db import models

# Create your models here.
from django.utils.text import slugify
from django.db.models.functions import Now  # Django 5.x
from django.db.models import Max


class BaseOrdenPublicado(models.Model):
    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True, db_default=Now())
    actualizado = models.DateTimeField(auto_now=True, db_default=Now())

    class Meta:
        abstract = True
        ordering = ["orden", "-creado"]


# 1) HERO / SLIDER
class HeroSlide(BaseOrdenPublicado):
    titulo = models.CharField(max_length=150)
    subtitulo = models.CharField(max_length=250, blank=True)
    boton1_texto = models.CharField(max_length=40, blank=True)
    boton1_url = models.URLField(blank=True)
    boton2_texto = models.CharField(max_length=40, blank=True)
    boton2_url = models.URLField(blank=True)
    imagen = models.ImageField(upload_to="inicio/hero/")

    class Meta(BaseOrdenPublicado.Meta):
        verbose_name = "1. Cabeceras / Hero Slides"
        verbose_name_plural = "1. Cabeceras / Hero Slides"

    def __str__(self):
        return self.titulo


# 2) VALORES / CARDS PEQUEÑAS CON ICONO
class ValorCard(BaseOrdenPublicado):
    titulo = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=200, blank=True)
    icono = models.ImageField(upload_to="inicio/icons/", blank=True, null=True)
    link_url = models.URLField(
        blank=True, help_text="URL a donde debe llevar este pilar (opcional)."
    )
    slug = models.SlugField(max_length=90, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)[:90]
        super().save(*args, **kwargs)

    class Meta(BaseOrdenPublicado.Meta):
        verbose_name = "2. Pilares / Value Cards"
        verbose_name_plural = "2. Pilares / Value Cards"

    def __str__(self):
        return self.titulo


# GALERIA INICIAL ULTIMOS EVENTOS


class Gallery(BaseOrdenPublicado):
    SECCIONES = [
        ("home_ultimos_eventos", "Home – Ultimos-Eventos"),
        ("nosotros_cabecera", "Nosotros – Cabecera"),
        ("proyectos_movimiento", "Home – Proyecto movimiento"),
        ("participa_estancias", "Participa – Estancias"),
    ]
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    seccion = models.CharField(
        max_length=50, choices=SECCIONES, default="home_ultimos_eventos"
    )
    descripcion = models.TextField(blank=True)
    descripcion_breve = models.CharField(
        max_length=200,
        blank=True,
        help_text="Texto corto que se muestra sobre la portada (tarjeta).",
    )
    portada = models.ImageField(upload_to="inicio/galerias/portadas/", blank=True)
    alt_portada = models.CharField(max_length=200, blank=True)

    class Meta(BaseOrdenPublicado.Meta):
        verbose_name = "3. Galerías / Galleries"
        verbose_name_plural = "3. Galerías / Galleries"
        # ⬅️ importante: para que las más nuevas (orden alto) salgan primero
        ordering = ["-orden", "-creado"]

    def save(self, *args, **kwargs):
        # Autogenerar 'orden' si está en 0, separado por seccion
        if self.orden == 0:
            max_orden = (
                Gallery.objects.filter(seccion=self.seccion).aggregate(Max("orden"))[
                    "orden__max"
                ]
                or 0
            )
            self.orden = max_orden + 1

        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class GalleryItem(BaseOrdenPublicado):
    galeria = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="items")
    titulo = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to="inicio/galerias/items/")
    alt = models.CharField(max_length=200, blank=True)
    credito = models.CharField(max_length=200, blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Separar por comas")

    class Meta(BaseOrdenPublicado.Meta):
        verbose_name = "Galeria ultimo evento item"
        verbose_name_plural = "Galeria ultimo evento item"

    def __str__(self):
        base = self.titulo or self.alt or self.imagen.name
        return f"{self.galeria.titulo} – {base}"


class SectionHeader(models.Model):
    SECCIONES = [
        ("home_ultimos_eventos", "Home – Últimos Eventos"),
        ("nosotros_cabecera", "Nosotros – Cabecera"),
        ("proyectos_movimiento", "Home – Proyectos en Movimiento"),
        ("participa_estancias", "Participa – Estancias"),
        ("tienda_tabs", "Tienda – Tabs"),
        ("home_cooperaciones", "cooperaciones – Tabs"),
    ]
    seccion = models.CharField(max_length=50, choices=SECCIONES, unique=True)
    title = models.CharField("Título (H2)", max_length=120)
    subtitle = models.CharField("Subtítulo (H5)", max_length=160, blank=True)
    limit = models.PositiveSmallIntegerField(default=12)
    publicado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Header de Sección"
        verbose_name_plural = "Headers de Sección"

    def __str__(self):
        return f"{self.get_seccion_display()} – {self.title}"
