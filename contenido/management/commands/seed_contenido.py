from pathlib import Path
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps


class Command(BaseCommand):
    help = "Asegura un flyer por defecto en Placement 'home_hero' (idempotente)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--once",
            action="store_true",
            help="No hace nada si el placement ya tiene flyer.",
        )

    def handle(self, *args, **opts):
        Placement = apps.get_model("contenido", "Placement")
        Flyer = apps.get_model("contenido", "Flyer")

        placement, _ = Placement.objects.get_or_create(
            key="home_hero",
            defaults={"activo": True},
        )

        if opts["once"] and placement.flyer_id:
            self.stdout.write(
                self.style.SUCCESS("Seed: ya existía flyer en home_hero.")
            )
            return

        if not placement.flyer_id:
            img_path = (
                Path(settings.BASE_DIR) / "core" / "static" / "seed" / "flyer-demo.jpg"
            )
            if not img_path.exists():
                self.stderr.write(f"No encuentro {img_path}")
                return

            flyer_kwargs = {"titulo": "Evento de ejemplo"}
            model_fields = {f.name for f in Flyer._meta.get_fields()}
            if "publicado" in model_fields:
                flyer_kwargs["publicado"] = True
            flyer = Flyer.objects.create(**flyer_kwargs)

            with img_path.open("rb") as fh:
                flyer.imagen.save("flyer-demo.jpg", File(fh), save=True)

            placement.flyer = flyer
            placement.activo = True
            placement.save(update_fields=["flyer", "activo"])

        self.stdout.write(self.style.SUCCESS("Seed: contenido por defecto OK."))
