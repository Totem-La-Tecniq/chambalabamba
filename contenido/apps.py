from django.apps import AppConfig


class ContenidoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "contenido"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "Contenido-Home"  # ← lo que quieres ver en el admin

    def ready(self):
        from django.db.models.signals import post_migrate
        from .seeders import _seed_footer_once

        post_migrate.connect(_seed_footer_once, sender=self)
