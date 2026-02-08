from django.core.management import call_command
from django.db import connection, transaction
from pathlib import Path

# (fixture, tag) — cada tag se guarda en la tabla seed_run para no recargar
SEEDS = [
    ("nosotros.json", "nosotros:v10"),  # el que ya tienes
    ("pilar_ecologia.json", "nosotros:pilar:ecologia:v3"),  # nuevo
    ("pilar_economia.json", "nosotros:pilar:economia:v2"),  # nuevo
    ("pilar_sociocultural.json", "nosotros:pilar:sociocultural:v2"),  # nuevo
    ("pilar_bienestar.json", "nosotros:pilar:bienestar:v2"),  # nuevo
    ("gobernanza.json", "nosotros:topic:gobernanza:v4"),
    ("principios_valores.json", "nosotros:topic:principios:v3"),
    ("territorio.json", "nosotros:topic:territorio:v2"),
]


def _seed_nosotros_once(sender, **kwargs):
    if sender.label != "nosotros":
        return

    base_dir = Path(__file__).resolve().parent
    with connection.cursor() as cur, transaction.atomic():
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")

        for filename, tag in SEEDS:
            # ¿ya corrido?
            cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [tag])
            if cur.fetchone():
                print(f"[seed_nosotros] Ya corrido {tag}, no se recarga")
                continue

            fixture_path = base_dir / "fixtures" / filename
            if not fixture_path.exists():
                print(f"[seed_nosotros] Omitido: no existe {fixture_path}")
                continue

            call_command("loaddata", str(fixture_path), verbosity=0)
            print(f"[seed_nosotros] Cargado fixture: {fixture_path.name}")

            cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [tag])
            print(f"[seed_nosotros] Marcado {tag}")
