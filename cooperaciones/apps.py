from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CooperacionesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cooperaciones"
    label = "cooperaciones"

    def ready(self):
        from .seeders import _seed_cooperaciones_once

        post_migrate.connect(
            _seed_cooperaciones_once,
            sender=self,
            dispatch_uid="coops_post_migrate_seed",
        )
