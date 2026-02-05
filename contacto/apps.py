from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ContactoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "contacto"

    def ready(self):
        from .seeders import _seed_contacto_once

        post_migrate.connect(_seed_contacto_once, sender=self)
