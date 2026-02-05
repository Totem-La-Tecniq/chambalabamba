from django.core.management import call_command
from django.db import connection, transaction
from pathlib import Path
from django.db.models.signals import post_migrate
from django.dispatch import receiver

SEED_TAG = "tienda:v7"  # súbelo (v2, v3, …) cuando quieras resembrar


@receiver(post_migrate)
def _seed_tienda_once(sender, **kwargs):
    # Correr solo cuando migra esta app
    if sender.name != "tienda":
        return

    with connection.cursor() as cur, transaction.atomic():
        # Tabla de control (si no existe)
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")

        # ¿Ya corrimos esta versión?
        cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [SEED_TAG])
        if cur.fetchone():
            print(f"[seed_tienda] Ya corrido {SEED_TAG}, no se recarga")
            return

        # Ruta a fixtures de la app tienda
        fixtures_dir = Path(__file__).resolve().parent / "fixtures"
        fixtures = [
            "tienda_seed.json",  # Categorías + Productos (usa imagen_portada)
            # "tienda_imagenes.json",  # (opcional) ProductoImagen si luego agregas galería
        ]

        # Carga en orden; si falta alguno, lo omite con aviso
        for fx in fixtures:
            path = fixtures_dir / fx
            if path.exists():
                call_command("loaddata", str(path), verbosity=0)
                print(f"[seed_tienda] Cargado fixture: {path.name}")
            else:
                print(f"[seed_tienda] Omitido (no existe): {path.name}")

        # Marcar como ejecutado
        cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [SEED_TAG])
        print(f"[seed_tienda] Marcado {SEED_TAG}")
