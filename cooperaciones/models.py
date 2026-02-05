from django.db import models
from django.urls import reverse


class CabeceraCoops(models.Model):
    h5 = models.CharField(
        "Subtítulo (h5)", max_length=120, default="Alianzas que nos potencian"
    )
    h2 = models.CharField("Título (h2)", max_length=140, default="Cooperaciones")
    subtitulo = models.CharField("Bajada (opcional)", max_length=200, blank=True)
    hero = models.ImageField(upload_to="coops/hero/", blank=True, null=True)
    publicado = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cabecera de Cooperaciones"
        verbose_name_plural = "Cabeceras de Cooperaciones"

    def __str__(self):
        return f"{self.h5} / {self.h2}"


class CoopCategoria(models.Model):
    nombre = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, unique=True)
    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "Categoría de cooperación"
        verbose_name_plural = "Categorías de cooperación"

    def __str__(self):
        return self.nombre


class Cooperacion(models.Model):
    categoria = models.ForeignKey(
        CoopCategoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="coops",
    )
    nombre = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    pais = models.CharField(max_length=80, blank=True)
    logo = models.ImageField(upload_to="coops/logos/", blank=True, null=True)
    portada = models.ImageField(upload_to="coops/portadas/", blank=True, null=True)
    excerpt = models.CharField(max_length=240, blank=True)
    descripcion = models.TextField(blank=True)
    url_externa = models.URLField(blank=True)

    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["orden", "-creado"]
        verbose_name = "Cooperación"
        verbose_name_plural = "Cooperaciones"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("coops:detalle", kwargs={"slug": self.slug})


class CoopFoto(models.Model):
    coop = models.ForeignKey(
        Cooperacion, related_name="fotos", on_delete=models.CASCADE
    )
    imagen = models.ImageField(upload_to="coops/fotos/")
    alt = models.CharField(max_length=140, blank=True)
    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "id"]
        verbose_name = "Foto de cooperación"
        verbose_name_plural = "Fotos de cooperación"

    def __str__(self):
        return f"{self.coop} – {self.alt or self.imagen.name}"
