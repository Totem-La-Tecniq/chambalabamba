# blog/seeds/seed_blog.py
from django.core.management import call_command
from django.db import connection, transaction
from pathlib import Path

FIXTURE_FILE = "blog_all.json"  # nombre del único JSON
SEED_TAG = "blog:all:v4"  # súbelo (v2, v3...) si quieres recargar


def _seed_blog_once(sender, **kwargs):
    if sender.label != "blog":
        return

    seeds_dir = Path(__file__).resolve().parent  # blog/seeds
    app_dir = seeds_dir.parent  # blog/
    candidates = [
        seeds_dir / "fixtures" / FIXTURE_FILE,  # blog/seeds/fixtures/blog_all.json
        app_dir / "fixtures" / FIXTURE_FILE,  # blog/fixtures/blog_all.json
    ]

    with connection.cursor() as cur, transaction.atomic():
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")
        cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [SEED_TAG])
        if cur.fetchone():
            print(f"[seed_blog] Ya corrido {SEED_TAG}, no se recarga")
            return

        fx_path = next((p for p in candidates if p.exists()), None)
        if not fx_path:
            print(f"[seed_blog] No se encontró {FIXTURE_FILE}")
            return

        call_command("loaddata", str(fx_path), verbosity=0)
        print(f"[seed_blog] Cargado {fx_path.name}")

        cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [SEED_TAG])
        print(f"[seed_blog] Marcado {SEED_TAG}")
