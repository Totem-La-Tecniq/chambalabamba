# blog/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
    verbose_name = "Blog"

    def ready(self):
        from .seeds.seed_blog import _seed_blog_once

        post_migrate.connect(_seed_blog_once, sender=self)
