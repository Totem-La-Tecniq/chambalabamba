from django.core.management import call_command
from django.db import connection, transaction
from pathlib import Path

SEEDS = [
    ("contacto_static_default.json", "contacto:static_default:v1"),
]


def _seed_contacto_once(sender, **kwargs):
    if sender.label != "contacto":
        return

    base_dir = Path(__file__).resolve().parent
    with connection.cursor() as cur, transaction.atomic():
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")

        for filename, tag in SEEDS:
            cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [tag])
            if cur.fetchone():
                print(f"[seed_contacto] Seed '{tag}' already run, skipping.")
                continue

            fixture_path = base_dir / "fixtures" / filename
            if not fixture_path.exists():
                print(
                    f"[seed_contacto] Skipped: Fixture '{fixture_path}' does not exist."
                )
                continue

            call_command("loaddata", str(fixture_path), verbosity=0)
            print(f"[seed_contacto] Loaded fixture: {fixture_path.name}")

            cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [tag])
            print(f"[seed_contacto] Marked '{tag}' as run.")

    print("[seed_contacto] Seeding process completed.")
