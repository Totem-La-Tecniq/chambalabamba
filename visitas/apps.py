# apps/visitas/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class VisitasConfig(AppConfig):
    name = "visitas"
    verbose_name = "Visitas guiadas"

    def ready(self):
        from .seeds.seed_visitas import _seed_visitas_once

        post_migrate.connect(_seed_visitas_once, sender=self)
