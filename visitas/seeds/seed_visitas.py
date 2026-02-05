# apps/visitas/seed_visitas.py
from django.core.management import call_command
from django.db import connection, transaction
from pathlib import Path

SEED_TAG = "visitas:v4"


def _seed_visitas_once(sender, **kwargs):
    with connection.cursor() as cur, transaction.atomic():
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")
        cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [SEED_TAG])
        if cur.fetchone():
            print(f"[seed_visitas] Ya corrido {SEED_TAG}")
            return

        fx = Path(__file__).resolve().parent / "fixtures" / "visitas_seed.json"
        if fx.exists():
            call_command("loaddata", str(fx), verbosity=0)
            print(f"[seed_visitas] Cargado {fx.name}")
        else:
            print("[seed_visitas] Fixture no encontrado:", fx)

        cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [SEED_TAG])
        print(f"[seed_visitas] Marcado {SEED_TAG}")
