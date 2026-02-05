from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command

from .models import Festival, Taller  # importa ambos modelos


@receiver(post_migrate)
def seed_eventos(sender, **kwargs):
    """
    Carga fixtures de la app eventos solo cuando:
      - La señal corresponde a esta app
      - La tabla está vacía (evita duplicados)
    El orden importa si hay FKs: primero festivales, luego talleres.
    """
    if sender.name != "eventos":
        return

    fixtures = [
        ("festivales", Festival),
        ("talleres", Taller),
    ]

    for fixture_name, model in fixtures:
        if model.objects.exists():
            continue  # ya hay datos, no recargar
        try:
            # busca en eventos/fixtures/<fixture_name>.json
            call_command("loaddata", fixture_name, verbosity=0)
            print(f"[seed_eventos] Cargado fixture: {fixture_name}")
        except Exception as e:
            print(f"[seed_eventos] No se pudo cargar {fixture_name}: {e}")
