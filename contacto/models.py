from django.db import models
from django.utils import timezone


class Contacto(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo Electrónico")
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Teléfono"
    )
    subject = models.CharField(max_length=200, verbose_name="Asunto")
    message = models.TextField(verbose_name="Mensaje")
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Fecha de envío"
    )

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Mensaje de {self.name} - {self.subject}"


class ContactoStatic(models.Model):
    titulo_superior = models.CharField(max_length=100, default="Contactar con")
    titulo = models.CharField(max_length=100, default="Ecoaldea Chambalabamba")
    blockquote_text = models.TextField(
        default="¿Tienes una semilla que quieras plantar con nosotros? Leeremos con atención tu mensaje y te responderemos con amor. ¡Gracias por acercarte a sembrar con nosotros!"
    )
    blockquote_footer = models.CharField(
        max_length=100, default="Ecoaldea Chambalabamba"
    )
    direccion = models.CharField(
        max_length=200, default="Via a Yamburara Alto, Vilcambamba, Ecuador"
    )
    telefono = models.CharField(max_length=20, default="+593980290103")
    email = models.EmailField(default="info@ecoaldeachambalabamba.org")
    google_maps_iframe = models.TextField(
        default='<iframe src="https.google.com/maps/embed?pb=!1m18!1m12!1m3!1d4667.746564849565!2d-79.20696632433055!3d-4.273985246192333!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x91cb2883c3dd5ff3%3A0x43f682d79e2d2dca!2sChambalabamba-Comunidad!5e1!3m2!1ses!2sde!4v1751679359755!5m2!1ses!2sde" allowfullscreen loading="lazy"></iframe>'
    )

    class Meta:
        verbose_name = "Página de Contacto"
        verbose_name_plural = "Página de Contacto"

    def __str__(self):
        return self.titulo
