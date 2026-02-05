# apps/donaciones/models.py
from django.db import models


class DonacionSection(models.Model):
    # Identificador para colocarla donde la necesites (ej. "home_callout")
    slug = models.SlugField(max_length=60, unique=True, help_text="Ej: home_callout")
    titulo_superior = models.CharField(max_length=120, default="Llamado Consciente")
    titulo = models.CharField(
        max_length=180, default="Sanación y Regeneración en Chambalabamba"
    )
    descripcion = models.TextField(
        default=(
            "En nuestra Ecocentro, practicamos la sanación y el cultivo de una "
            "conciencia ecológica y espiritual. Tu apoyo nos ayuda a expandir este "
            "espacio de transformación, donde la tierra y el ser se armonizan."
        )
    )
    cta_titulo = models.CharField(max_length=120, default="Apoya este Espacio")
    cta_boton_texto = models.CharField(max_length=60, default="Contribuir con Amor")
    cta_placeholder_otro = models.CharField(max_length=40, default="$ Otro")

    # New fields for admin-manageable content
    intro_text = models.TextField(
        blank=True, null=True, help_text="Introductory text for the main donation page."
    )
    # Setting a default image path. User will need to ensure this file exists or provide their own.
    donation_image = models.ImageField(
        upload_to="donations/",
        blank=True,
        null=True,
        default="donations/default_donation_image.png",
        help_text="Image for the main donation page. Defaults to 'donations/default_donation_image.png'.",
    )
    success_title = models.CharField(
        max_length=120, default="¡Gracias por tu donación!"
    )
    success_message = models.TextField(
        default="Tu donación ha sido procesada exitosamente. Agradecemos tu apoyo."
    )
    canceled_title = models.CharField(max_length=120, default="Donación Cancelada")
    canceled_message = models.TextField(
        default="Tu donación ha sido cancelada. Si tienes algún problema, por favor, contáctanos."
    )
    paypal_redirect_message = models.TextField(
        default="Por favor, espera mientras te redirigimos a PayPal para completar tu donación."
    )

    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "slug"]
        verbose_name = "Sección de Donaciones / Donations Section"
        verbose_name_plural = "Secciones de Donaciones / Donations Sections"

    def __str__(self):
        return f"{self.slug} – {self.titulo}"


class DonacionMonto(models.Model):
    section = models.ForeignKey(
        DonacionSection, on_delete=models.CASCADE, related_name="montos"
    )
    # Guarda el valor como entero en centavos o como texto. Aquí simple:
    etiqueta = models.CharField(max_length=20, help_text='Ej: "$100"')
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "id"]
        verbose_name = "Monto sugerido / Suggested Amount"
        verbose_name_plural = "Montos sugeridos / Suggested Amounts"

    def __str__(self):
        return f"{self.section.slug}: {self.etiqueta}"


class Donacion(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    paypal_id = models.CharField(max_length=100, blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)


def __str__(self):
    return f"Donación de {self.nombre} por {self.monto}"


class DonacionesStatic(models.Model):
    titulo = models.CharField(max_length=200, default="Apoyo a Chambalabamba")
    contenido = models.TextField(
        help_text="Contenido principal de la página de donaciones. Puedes usar HTML si es necesario.",
        default="<p>Para realizar una donación y apoyar nuestros proyectos, por favor contáctanos a través de...</p>",
    )
    email_contacto = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        help_text="Correo electrónico de contacto para donaciones.",
    )
    telefono_contacto = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Teléfono de contacto para donaciones.",
    )
    imagen = models.ImageField(
        upload_to="donaciones_static/",
        blank=True,
        null=True,
        help_text="Imagen opcional para la página de donaciones.",
    )
    publicado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Página de Donaciones"
        verbose_name_plural = "Páginas de Donaciones"

    def __str__(self):
        return self.titulo
