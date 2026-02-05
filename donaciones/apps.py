from django.apps import AppConfig
from django.db.models.signals import post_migrate


class DonacionesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "donaciones"

    def ready(self):
        from .seeders import _seed_donaciones_once

        post_migrate.connect(_seed_donaciones_once, sender=self)
