from django.core.management import call_command
from django.db import connection, transaction
from pathlib import Path

# Cambia el nombre si usas otro archivo
FIXTURE_FILE = "proyectos_all.json"
SEED_TAG = "proyectos:all:v1"  # súbelo (v2, v3...) cuando quieras recargar


def _seed_proyectos_once(sender, **kwargs):
    # Ejecuta solo cuando migra la app 'proyectos'
    if sender.label != "proyectos":
        return

    seeds_dir = Path(__file__).resolve().parent  # proyectos/seeds
    app_dir = seeds_dir.parent  # proyectos/
    candidates = [
        seeds_dir / "fixtures" / FIXTURE_FILE,  # proyectos/seeds/fixtures/...
        app_dir / "fixtures" / FIXTURE_FILE,  # proyectos/fixtures/...
        Path.cwd() / "fixtures" / FIXTURE_FILE,  # <raíz>/fixtures/...
    ]

    with connection.cursor() as cur, transaction.atomic():
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")
        cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [SEED_TAG])
        if cur.fetchone():
            print(f"[seed_proyectos] Ya corrido {SEED_TAG}, no se recarga")
            return

        fx_path = next((p for p in candidates if p.exists()), None)
        if not fx_path:
            print(f"[seed_proyectos] No se encontró {FIXTURE_FILE} en {candidates}")
            return

        call_command("loaddata", str(fx_path), verbosity=0)
        print(f"[seed_proyectos] Cargado: {fx_path}")

        cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [SEED_TAG])
        print(f"[seed_proyectos] Marcado {SEED_TAG}")
