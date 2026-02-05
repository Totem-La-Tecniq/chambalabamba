from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group
from django.utils.text import slugify
from django.core.validators import RegexValidator


class TipoUsuario(models.Model):
    """
    Rol extensible desde el admin. Cada TipoUsuario se asocia 1–1 a un Group
    para gestionar permisos. Puedes crear más tipos (p.ej. 'editor', 'moderador')
    y asignarles permisos via Group.
    """

    nombre = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(
        max_length=30,
        unique=True,
        blank=True,
        null=True,
        help_text="Identificador único (ej. 'externo', 'residente').",
    )

    descripcion = models.TextField(blank=True)

    # Grupo de permisos asociado a este rol (se crea automáticamente en signals)
    role_group = models.OneToOneField(
        Group,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="Grupo de permisos asociado a este rol.",
        related_name="tipo_usuario",
    )

    class Meta:
        verbose_name = "Tipo de usuario"
        verbose_name_plural = "Tipos de usuario"
        ordering = ["nombre"]
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    @classmethod
    def get_externo_pk(cls):
        """
        Garantiza que exista el rol 'externo' y devuelve su PK.
        Útil como default en ForeignKey sin depender de datos precargados.
        """
        obj, _ = cls.objects.get_or_create(
            slug="externo",
            defaults={
                "nombre": "Externo",
                "descripcion": "Usuario externo por defecto",
            },
        )
        return obj.pk


# Validador simple opcional para teléfonos (puedes quitarlo si no lo necesitas)
phone_validator = RegexValidator(
    regex=r"^[\d\-\+\(\) ]{6,30}$",
    message="Ingresa un teléfono válido (6–30 caracteres).",
)


class PerfilUsuario(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfilusuario",  # se mantiene para compatibilidad con tu código
    )

    # Hacemos el tipo obligatorio con default a 'externo' (no null/no blank)
    tipo_usuario = models.ForeignKey(
        TipoUsuario,
        on_delete=models.PROTECT,
        default=TipoUsuario.get_externo_pk,
        related_name="perfiles",
    )

    # 👇 agrega este campo
    display_name = models.CharField("Nombre público", max_length=150, blank=True)

    telefono = models.CharField(max_length=30, blank=True, validators=[phone_validator])
    bio = models.TextField(blank=True)

    # Timestamps útiles
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    rol_en_comunidad = models.CharField(max_length=100, blank=True)
    areas_aporte = models.CharField(
        max_length=200, blank=True
    )  # o ManyToMany a etiquetas
    disponibilidad = models.CharField(max_length=100, blank=True)
    fecha_residencia_desde = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuario"
        indexes = [
            models.Index(fields=["tipo_usuario"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Perfil de {self.user.username}"

    # Helpers de rol (prácticos en vistas/plantillas)
    @property
    def es_residente(self) -> bool:
        return getattr(self.tipo_usuario, "slug", None) == "residente"

    @property
    def es_externo(self) -> bool:
        return getattr(self.tipo_usuario, "slug", None) == "externo"
