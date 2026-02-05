# apps/autenticacion/signals.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, post_migrate, pre_save
from django.dispatch import receiver
from django.db.utils import ProgrammingError, OperationalError
from django.apps import apps

from .models import TipoUsuario, PerfilUsuario

User = get_user_model()
ROLE_PREFIX = "role:"


def role_group_name(slug: str) -> str:
    return f"{ROLE_PREFIX}{slug or 'externo'}"


# ─────────────────────────────────────────────────────────────
# 1) Sembrar tipos base y sus grupos DESPUÉS de migrar esta app
#    (envuelto en try/except por si es el primer arranque)
# ─────────────────────────────────────────────────────────────
@receiver(post_migrate)
def seed_tipos_and_groups(sender, **kwargs):
    # Ejecutar solo cuando termina de migrar *esta* app
    if getattr(sender, "name", "") != "autenticacion":
        return

    try:
        # Reobtén el modelo por si el import normal aún no está del todo listo
        TipoUsuario = apps.get_model("autenticacion", "TipoUsuario")

        # Si por alguna razón el campo 'slug' aún no existe, sal silenciosamente
        field_names = {f.name for f in TipoUsuario._meta.get_fields()}
        if "slug" not in field_names:
            return

        externo, _ = TipoUsuario.objects.get_or_create(
            slug="externo",
            defaults={
                "nombre": "Externo",
                "descripcion": "Usuario externo por defecto",
            },
        )
        residente, _ = TipoUsuario.objects.get_or_create(
            slug="residente",
            defaults={"nombre": "Residente", "descripcion": "Usuario residente"},
        )

        # Asegura grupos por rol
        for tipo in (externo, residente):
            if not tipo.role_group_id:
                g, _ = Group.objects.get_or_create(name=role_group_name(tipo.slug))
                tipo.role_group = g
                tipo.save(update_fields=["role_group"])

    except (ProgrammingError, OperationalError):
        # DB/tables aún no listas (primer arranque). Ignorar.
        pass


# ─────────────────────────────────────────────────────────────
# 2) Mantener coherencia grupo↔slug al editar Tipos
# ─────────────────────────────────────────────────────────────
@receiver(pre_save, sender=TipoUsuario)
def rename_group_if_slug_changes(sender, instance: TipoUsuario, **kwargs):
    # solo si ya existe en BD
    if not instance.pk:
        return
    try:
        old = TipoUsuario.objects.get(pk=instance.pk)
    except TipoUsuario.DoesNotExist:
        return

    if old.slug != instance.slug and instance.role_group_id:
        instance.role_group.name = role_group_name(instance.slug)
        instance.role_group.save(update_fields=["name"])


@receiver(post_save, sender=TipoUsuario)
def ensure_group_for_tipo(sender, instance: TipoUsuario, created, **kwargs):
    if not instance.role_group_id:
        g, _ = Group.objects.get_or_create(name=role_group_name(instance.slug))
        instance.role_group = g
        instance.save(update_fields=["role_group"])


# ─────────────────────────────────────────────────────────────
# 3) Crear PerfilUsuario al crear User (tipo por defecto = 'externo')
# ─────────────────────────────────────────────────────────────
@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance: User, created, **kwargs):
    if created:
        PerfilUsuario.objects.get_or_create(user=instance)


# ─────────────────────────────────────────────────────────────
# 4) Sincronizar grupos del usuario al guardar su Perfil
# ─────────────────────────────────────────────────────────────
def _sync_user_role_group(user: User):
    # Quita todos los grupos de rol previos
    role_groups = Group.objects.filter(name__startswith=ROLE_PREFIX)
    if role_groups.exists():
        user.groups.remove(*role_groups)

    # Añade el grupo del tipo actual (si existe)
    try:
        perfil = user.perfilusuario  # related_name
    except PerfilUsuario.DoesNotExist:
        return

    if perfil.tipo_usuario and perfil.tipo_usuario.role_group_id:
        user.groups.add(perfil.tipo_usuario.role_group)


@receiver(post_save, sender=PerfilUsuario)
def sync_role_group_on_profile_save(sender, instance: PerfilUsuario, **kwargs):
    if instance.user_id:
        _sync_user_role_group(instance.user)
