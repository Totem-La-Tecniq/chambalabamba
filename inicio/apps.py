# apps/inicio/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class InicioConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "inicio"

    def ready(self):
        # Conectar el seeder para correr tras migraciones de esta app
        from .seeders import seed_inicio_once

        post_migrate.connect(seed_inicio_once, sender=self)
