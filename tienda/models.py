from django.db import models
from django.urls import reverse


class TiendaLanding(models.Model):
    publicado = models.BooleanField(default=True)
    title = models.CharField(max_length=160, default="Tienda")
    intro_html = models.TextField(blank=True, help_text="Texto de bienvenida (HTML).")
    cta_text = models.CharField(max_length=60, blank=True, default="Ver productos")
    cta_url = models.CharField(
        max_length=200, blank=True, default="/tienda/"
    )  # ajusta si tu ruta difiere

    class Meta:
        verbose_name = "Página de Tienda (landing)"
        verbose_name_plural = "Página de Tienda (landing)"

    def __str__(self):
        return "Landing de Tienda"


class ProductoCategoria(models.Model):
    nombre = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=0)
    publicado = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "2. Categoría de producto"
        verbose_name_plural = "2. Categorías de producto"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        ProductoCategoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos",
    )
    titulo = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    descripcion_corta = models.CharField(max_length=240, blank=True)
    descripcion = models.TextField(blank=True)

    imagen_portada = models.ImageField(
        upload_to="productos/portadas/", blank=True, null=True
    )

    # Precios (puedes migrarlo a Decimal con 2 decimales si quieres exactitud)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_tachado = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        # Ajusta al nombre real de tu ruta de detalle si existe:
        return reverse("tienda:detalle-producto", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["orden", "-creado"]
        verbose_name = "1) Producto"
        verbose_name_plural = "1) Productos"

    def __str__(self):
        return self.titulo


class ProductoImagen(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="imagenes"
    )
    imagen = models.ImageField(upload_to="productos/items/")
    alt = models.CharField(max_length=140, blank=True)
    orden = models.PositiveIntegerField(default=0)
    publicado = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "id"]
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imágenes de producto"

    def __str__(self):
        return f"{self.producto.titulo} – {self.alt or self.imagen.name}"


# Create your models here.
