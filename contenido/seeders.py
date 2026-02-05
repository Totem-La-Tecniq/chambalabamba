from django.core.management import call_command
from django.db import connection, transaction

SEED_TAG = "footer:v1"  # súbelo a v2, v3... cuando quieras resembrar


def _seed_footer_once(sender, **kwargs):
    with connection.cursor() as cur, transaction.atomic():
        # 1) Ledger de seeds
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")

        # 2) ¿Ya corrimos esta versión?
        cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [SEED_TAG])
        if cur.fetchone():
            print(f"[seed_footer] Ya corrido {SEED_TAG}, no se recarga")
            return

        # 3) Cargar fixtures (en orden si tuvieras varios)
        fixtures = ["footer_initial"]  # contenido/fixtures/footer_initial.json
        for fx in fixtures:
            call_command("loaddata", fx, verbosity=0)
            print(f"[seed_footer] Cargado fixture: {fx}")

        # 4) Registrar versión
        cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [SEED_TAG])
        print(f"[seed_footer] Marcado {SEED_TAG}")
