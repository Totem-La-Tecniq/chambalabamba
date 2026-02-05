# apps/autenticacion/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import PerfilUsuario, TipoUsuario

User = get_user_model()


# ────────────────────────────────────────────────────────────────────────────────
# 1) SIGNUP: usuario externo por defecto (sin exponer el tipo)
#    Incluye campos útiles para un ecocentro: nombre, email y datos básicos de perfil.
# ────────────────────────────────────────────────────────────────────────────────
class SignupForm(UserCreationForm):
    # Campos de User
    first_name = forms.CharField(label="Nombres", max_length=150, required=False)
    last_name = forms.CharField(label="Apellidos", max_length=150, required=False)
    email = forms.EmailField(label="Correo", required=True)

    # Campos de PerfilUsuario (se guardan en el perfil)
    display_name = forms.CharField(
        label="Nombre público",
        max_length=150,
        required=False,
        help_text="Cómo quieres que te vean en el sitio.",
    )
    telefono = forms.CharField(
        label="Teléfono",
        max_length=30,
        required=False,
        help_text="Para coordinaciones (opcional).",
    )
    bio = forms.CharField(
        label="Sobre ti",
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
        help_text="Cuéntanos brevemente quién eres (opcional).",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # OJO: Solo campos del User van en Meta.fields
        fields = ("username", "first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip()
        if not email:
            raise ValidationError("El correo es obligatorio.")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Ya existe un usuario con este correo.")
        return email

    def save(self, commit=True):
        """
        Crea el User y actualiza su PerfilUsuario.
        Por defecto, el Perfil queda con tipo 'externo' (lo asegura el modelo/signals).
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()

        # Asegura que exista el perfil (tus signals ya lo crean, pero por si acaso)
        perfil, _ = PerfilUsuario.objects.get_or_create(user=user)

        # Setea datos del perfil
        perfil.display_name = self.cleaned_data.get("display_name", "")
        perfil.telefono = self.cleaned_data.get("telefono", "")
        perfil.bio = self.cleaned_data.get("bio", "")
        perfil.save()

        return user


# ────────────────────────────────────────────────────────────────────────────────
# 2) PERFILES: formularios según rol
#    - Externo: datos básicos visibles públicos
#    - Residente: mismos datos por ahora (puedes ampliar con más campos en el modelo)
# ────────────────────────────────────────────────────────────────────────────────
class PerfilExternoForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ("display_name", "telefono", "bio")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {
            "display_name": "Nombre público con el que te mostrará el sitio.",
            "telefono": "Para coordinaciones internas (opcional).",
            "bio": "Una breve descripción (opcional).",
        }


class PerfilResidenteForm(forms.ModelForm):
    """
    Si más adelante agregas campos específicos de residente al modelo (por ejemplo:
    fecha_residencia_desde, area_aporte, disponibilidad), solo añádelos aquí a 'fields'.
    """

    class Meta:
        model = PerfilUsuario
        fields = (
            "display_name",
            "telefono",
            "bio",
            "rol_en_comunidad",
            "areas_aporte",
            "disponibilidad",
            "fecha_residencia_desde",
        )
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
        help_texts = {
            "display_name": "Nombre visible para la comunidad.",
            "telefono": "Teléfono de contacto interno.",
            "bio": "Breve presentación como residente.",
        }


# ────────────────────────────────────────────────────────────────────────────────
# 3) Cambio de rol (solo staff): ascender/ajustar tipo_usuario
#    No lo uses en formularios públicos.
# ────────────────────────────────────────────────────────────────────────────────
class PerfilRoleForm(forms.ModelForm):
    """
    Form para uso interno (staff). Permite cambiar el tipo_usuario.
    Tus signals sincronizan los grupos automáticamente.
    """

    tipo_usuario = forms.ModelChoiceField(
        label="Rol",
        queryset=TipoUsuario.objects.all(),
        required=True,
        help_text="Selecciona el rol del usuario (ej. Externo, Residente).",
    )

    class Meta:
        model = PerfilUsuario
        fields = ("tipo_usuario",)


class PerfilUpdateForm(forms.ModelForm):
    """
    Form dinámico para actualizar el perfil.
    - Si tipo = 'residente'  → muestra campos extra (rol_en_comunidad, …)
    - Si tipo = 'externo'    → oculta esos campos y los limpia al guardar
    """

    class Meta:
        model = PerfilUsuario
        fields = (
            "tipo_usuario",  # el usuario puede cambiar su tipo si lo permites
            "display_name",
            "telefono",
            "bio",
            "rol_en_comunidad",
            "areas_aporte",
            "disponibilidad",
            "fecha_residencia_desde",
        )
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
            "fecha_residencia_desde": forms.DateInput(attrs={"type": "date"}),
        }
        help_texts = {
            "display_name": "Nombre público con el que se te mostrará en el sitio.",
        }

    # Campos exclusivos de residentes
    RESIDENT_ONLY = (
        "rol_en_comunidad",
        "areas_aporte",
        "disponibilidad",
        "fecha_residencia_desde",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Descubre el tipo seleccionado (POST) o el del instance (GET)
        tipo_obj = None
        tipo_id = self.data.get("tipo_usuario")
        if tipo_id:
            try:
                tipo_obj = TipoUsuario.objects.get(pk=tipo_id)
            except TipoUsuario.DoesNotExist:
                pass
        if not tipo_obj and getattr(self.instance, "tipo_usuario_id", None):
            tipo_obj = self.instance.tipo_usuario

        slug = getattr(tipo_obj, "slug", "externo")

        # Por defecto todo opcional
        for name in self.fields:
            self.fields[name].required = False

        # Decide qué campos se renderizan
        base_fields = {"tipo_usuario", "display_name", "telefono", "bio"}
        if slug == "residente":
            allowed = base_fields | set(self.RESIDENT_ONLY)

            # Si quieres exigir algunos campos de residente, márcalos aquí:
            # self.fields["rol_en_comunidad"].required = True
            # self.fields["fecha_residencia_desde"].required = True
        else:
            allowed = base_fields

        # Elimina de la forma los que no aplican al tipo actual (no se renderizan)
        for name in list(self.fields.keys()):
            if name not in allowed:
                self.fields.pop(name)

    def clean(self):
        cleaned = super().clean()
        # Puedes añadir validaciones condicionales aquí si marcaste alguno como requerido
        # p.ej. si es residente y falta 'rol_en_comunidad', add_error(...)
        return cleaned

    def save(self, commit=True):
        obj: PerfilUsuario = super().save(commit=False)
        slug = getattr(obj.tipo_usuario, "slug", "externo")
        if slug != "residente":
            # Limpia campos que no aplican al cambiar a 'externo'
            obj.rol_en_comunidad = ""
            obj.areas_aporte = ""
            obj.disponibilidad = ""
            obj.fecha_residencia_desde = None
        if commit:
            obj.save()
        return obj
