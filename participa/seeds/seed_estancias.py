# apps/estancias/seeds/seed_estancias.py
from django.core.management import call_command
from django.db import connection, transaction
from django.conf import settings
from pathlib import Path

SEED_TAG = "estancias:v13"  # <- súbelo al cambiar el seed/datos


def _seed_estancias_once(sender, **kwargs):
    with connection.cursor() as cur, transaction.atomic():
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")
        cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [SEED_TAG])
        if cur.fetchone():
            print(f"[seed_estancias] Ya corrido {SEED_TAG}, no se recarga")
            return

        # Archivos a intentar cargar (en este orden)
        fixtures = [
            "estancias.json",
            "estancias_fotos.json",
            "estancias_specs.json",
            "estancias_intro.json",
        ]

        # Carpetas candidatas donde buscarlos
        seeds_dir = Path(__file__).resolve().parent  # apps/estancias/seeds
        estancias_app = seeds_dir.parent  # apps/estancias
        participa_app = estancias_app.parent / "participa"  # apps/participa
        candidate_dirs = [
            estancias_app / "fixtures",  # apps/estancias/fixtures
            seeds_dir / "fixtures",  # apps/estancias/seeds/fixtures
            participa_app / "fixtures",  # apps/participa/fixtures  <-- tu caso actual
        ]
        # También respeta FIXTURE_DIRS si lo usas en settings.py
        for p in getattr(settings, "FIXTURE_DIRS", []):
            candidate_dirs.append(Path(p))

        # Intenta cargar por ruta exacta; si no está, intenta por nombre (loaddata estándar)
        def try_load(path_or_name: str):
            try:
                call_command("loaddata", path_or_name, verbosity=0)
                print(f"[seed_estancias] Cargado: {path_or_name}")
                return True
            except Exception as e:
                print(f"[seed_estancias] Omitido {path_or_name}: {e}")
                return False

        # Carga cada fixture
        for fx in fixtures:
            loaded = False
            for d in candidate_dirs:
                p = d / fx
                if p.exists():
                    if try_load(str(p)):
                        loaded = True
                        break
            if not loaded:
                # último intento: por nombre (Django buscará en apps registradas)
                try_load(fx)

        cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [SEED_TAG])
        print(f"[seed_estancias] Marcado {SEED_TAG}")
