from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .seeders import _seed_tienda_once


class TiendaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tienda"

    def ready(self):
        # Importa el seeder para registrar el post_migrate
        from . import seeders  # noqa

        post_migrate.connect(_seed_tienda_once, sender=self)
