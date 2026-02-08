from django.core.management import call_command
from django.db import connection, transaction
from pathlib import Path

APP_LABEL = "cooperaciones"

# (fixture, tag) — cada tag se guarda en seed_run para no recargarlo dos veces
SEEDS = [
    ("coops_seed.json", "coops:v3"),
    # Si más adelante sumas otras semillas (p. ej. por países), agrega sus tags aquí:
    # ("coops_seed_extra.json", "coops:extra:v1"),
]

# Tag para el copiado de media (imágenes) por única vez
MEDIA_SEED_TAG = "coops:media:v1"


def _load_fixtures_once(base_dir):
    with connection.cursor() as cur, transaction.atomic():
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")

        for filename, tag in SEEDS:
            # ¿ya corrido este seed?
            cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [tag])
            if cur.fetchone():
                print(f"[seed_coops] Ya corrido {tag}, no se recarga")
                continue

            fixture_path = (base_dir / "fixtures" / filename).resolve()
            if not fixture_path.exists():
                print(f"[seed_coops] Omitido: no existe {fixture_path}")
                continue

            call_command("loaddata", str(fixture_path), verbosity=0)
            print(f"[seed_coops] Cargado fixture: {fixture_path.name}")

            cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [tag])
            print(f"[seed_coops] Marcado tag {tag}")


def _seed_cooperaciones_once(sender, **kwargs):
    # Se asegura de ejecutar solo cuando migra la app cooperaciones
    if sender.label != APP_LABEL:
        return
    base_dir = Path(__file__).resolve().parent
    _load_fixtures_once(base_dir)
