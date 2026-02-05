from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


def _copy_media_after_migrate(sender, **kwargs):
    # Evita correr si así lo indicas en settings
    if not getattr(settings, "COPY_SEED_MEDIA_ON_MIGRATE", True):
        return
    from .utils.seed_media import copy_seed_media  # import local para evitar ciclos

    try:
        n = copy_seed_media(force=False)
        print(f"[seed_media] Copiados {n} archivos a MEDIA_ROOT")
    except Exception as e:
        print(f"[seed_media] Error al copiar media semilla: {e}")


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        post_migrate.connect(_copy_media_after_migrate, sender=self)
