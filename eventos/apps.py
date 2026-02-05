from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .seeders import (
    _seed_eventos_once,
)  # lo defines en otro archivo (ej. seed_proyectos.py)


class EventosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "eventos"  # ← debe coincidir con la carpeta real
    label = "eventos"  # ← opcional pero recomendable

    def ready(self):
        post_migrate.connect(_seed_eventos_once, sender=self)
