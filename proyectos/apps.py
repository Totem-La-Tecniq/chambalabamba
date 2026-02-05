from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ProyectosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "proyectos"
    verbose_name = "Proyectos"

    def ready(self):
        from .seeds.seed_proyectos import _seed_proyectos_once

        post_migrate.connect(_seed_proyectos_once, sender=self)
