# apps/inicio/seed_proyectos.py
from django.core.management import call_command
from django.db import connection, transaction
from pathlib import Path
import os

# Sube la versión para resembrar (p.ej. v2, v3...)
SEED_TAG = os.getenv("INICIO_SEED_TAG", "inicio:v21")
FIXTURE_FILENAME = os.getenv("INICIO_FIXTURE", "inicio_seed.json")


def seed_inicio_once(sender, **kwargs):
    """
    Carga el fixture de inicio una sola vez por BD.
    - Crea tabla seed_run si no existe
    - Verifica tag para evitar recargas
    - Carga el fixture JSON desde apps/inicio/fixtures/
    """
    with connection.cursor() as cur, transaction.atomic():
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")
        cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [SEED_TAG])
        if cur.fetchone():
            print(f"[seed_inicio] Ya corrido {SEED_TAG}, no se recarga")
            return

        fixture_path = Path(__file__).resolve().parent / "fixtures" / FIXTURE_FILENAME
        if not fixture_path.exists():
            print(f"[seed_inicio] ERROR: Fixture no encontrado -> {fixture_path}")
            return

        call_command("loaddata", str(fixture_path), verbosity=0)
        print(f"[seed_inicio] Cargado fixture: {fixture_path.name}")

        cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [SEED_TAG])
        print(f"[seed_inicio] Marcado {SEED_TAG}")
