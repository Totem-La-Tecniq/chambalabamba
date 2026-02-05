# core/management/commands/load_seed_media.py
from django.core.management.base import BaseCommand
from core.utils.seed_media import copy_seed_media


class Command(BaseCommand):
    help = "Copia imágenes semilla hacia MEDIA_ROOT"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true")

    def handle(self, *args, **opts):
        n = copy_seed_media(force=opts["force"])
        self.stdout.write(self.style.SUCCESS(f"Copiados {n} archivos"))
