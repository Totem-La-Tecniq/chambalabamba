# core/models.py
from django.db import models


class PageHeader(models.Model):
    slug = models.SlugField(unique=True)  # ej: "voluntariado"
    title = models.CharField(max_length=150, blank=True, default="")
    subtitle = models.CharField(max_length=200, blank=True, default="")
    background = models.ImageField(upload_to="headers/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.slug
