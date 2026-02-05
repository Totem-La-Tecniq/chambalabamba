# apps/nosotros/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .seeders import _seed_nosotros_once


class NosotrosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nosotros"
    label = "nosotros"

    def ready(self):
        post_migrate.connect(_seed_nosotros_once, sender=self)
