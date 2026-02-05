from django.core.management import call_command
from django.db import connection, transaction

SEED_TAG = "eventos:v5"  # cámbialo a v5 cuando quieras resembrar


def _seed_eventos_once(sender, **kwargs):
    with connection.cursor() as cur, transaction.atomic():
        # Crear tabla ledger si no existe
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")
        # Verificar si ya corrimos esta versión
        cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [SEED_TAG])
        if cur.fetchone():
            print(f"[seed_eventos] Ya corrido {SEED_TAG}, no se recarga")
            return

        # Cargar fixtures en orden
        fixtures = [
            "festivales",
            "talleres",
            "talleres_page",
            "festivales_page",
            "artes_page",
            "escuela_page",
            "retiros_page",
            "terapias_page",
        ]
        for fx in fixtures:
            call_command("loaddata", fx, verbosity=0)
            print(f"[seed_eventos] Cargado fixture: {fx}")

        # Registrar versión
        cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [SEED_TAG])
        print(f"[seed_eventos] Marcado {SEED_TAG}")
