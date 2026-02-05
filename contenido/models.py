from django.db.models import JSONField

# Create your models here.
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.urls import reverse


class MediaAsset(models.Model):
    titulo = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to="media/")
    alt = models.CharField(max_length=200, blank=True)
    credito = models.CharField(max_length=200, blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Separar por comas")
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Gallery(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    publicado = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Galerías de Inicio/Home"
        verbose_name_plural = "Galeria de Inicio/Home"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class GalleryItem(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="items")
    asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE)
    caption = models.CharField(max_length=250, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return f"{self.gallery} · {self.asset} ({self.orden})"


class Flyer(models.Model):
    class Meta:
        verbose_name_plural = "Flyers de Inicio/Home"
        verbose_name_plural = "Flyers de Inicio/Home"

    RATIO_CHOICES = [
        ("1x1", "1:1"),
        ("4x5", "4:5 (IG 1080×1350)"),
        ("16x9", "16:9 (1920×1080)"),
        ("9x16", "9:16 (stories)"),
    ]
    titulo = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to="flyers/")
    ratio = models.CharField(max_length=5, choices=RATIO_CHOICES, default="4x5")
    alt = models.CharField(max_length=200, blank=True)
    publicado = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Placement(models.Model):
    """
    Slot reutilizable por clave. Uno de los dos campos apunta al contenido.
    Ej: key='home_hero' -> flyer destacado; key='galeria_footer' -> gallery.
    """

    key = models.SlugField(unique=True, help_text="Ej: home_hero, galeria_footer")
    flyer = models.ForeignKey(Flyer, null=True, blank=True, on_delete=models.SET_NULL)
    gallery = models.ForeignKey(
        Gallery, null=True, blank=True, on_delete=models.SET_NULL
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.key


# bloques para administrar el footer #


class FooterSettings(models.Model):
    """Bloque: 'Sobre Chambalabamba'."""

    title = models.CharField(max_length=120, default="Sobre Chambalabamba")
    text = models.TextField(
        default=(
            "Una ecoaldea viva en Vilcabamba donde florece la libertad, el arte y la conciencia. "
            "Promovemos un estilo de vida autosostenible y en armonía con la Tierra."
        )
    )
    link_label = models.CharField(max_length=80, default="Conócenos")
    # opciones de link: url absoluto/relativo o nombre de url + kwargs
    url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Puede ser ruta relativa ('/nosotros/') o absoluta.",
    )
    named_url = models.CharField(
        max_length=120,
        blank=True,
        help_text="Nombre de URL de Django (toma prioridad si está). Ej: 'nosotros:nuestro_camino'",
    )
    named_url_kwargs = JSONField(
        blank=True,
        null=True,
        help_text="Opcional: kwargs para reverse() en JSON. Ej: {'slug':'filosofia'}",
    )
    open_in_new_tab = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Footer – Sobre Chambalabamba"
        verbose_name_plural = "Footer – Sobre Chambalabamba"

    def __str__(self):
        return self.title

    def resolved_href(self):
        if self.named_url:
            try:
                return reverse(self.named_url, kwargs=self.named_url_kwargs or {})
            except Exception:
                return "#"
        return self.url or "#"


class FooterMenu(models.Model):
    """Columna de links (ej: 'Nuestra propuesta')."""

    name = models.CharField(max_length=120, default="Nuestra propuesta")
    order = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Footer – Menú"
        verbose_name_plural = "Footer – Menús"

    def __str__(self):
        return self.name


class FooterLink(models.Model):
    menu = models.ForeignKey(FooterMenu, on_delete=models.CASCADE, related_name="links")
    label = models.CharField(max_length=150)
    # mismas opciones que arriba
    url = models.CharField(max_length=255, blank=True)
    named_url = models.CharField(max_length=120, blank=True)
    named_url_kwargs = JSONField(blank=True, null=True)
    open_in_new_tab = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Footer – Link"
        verbose_name_plural = "Footer – Links"

    def __str__(self):
        return f"{self.menu.name} · {self.label}"

    def href(self):
        if self.named_url:
            try:
                return reverse(self.named_url, kwargs=self.named_url_kwargs or {})
            except Exception:
                return "#"
        return self.url or "#"
