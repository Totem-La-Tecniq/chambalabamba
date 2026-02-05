# participa/seeds/seed_voluntariado.py
from django.core.management import call_command, CommandError
from django.db import connection, transaction
from django.conf import settings
from pathlib import Path

SEED_TAG = "voluntariado:v12"  # súbelo cuando cambies datos
FIXTURE_BASENAME = "voluntariado_fixture"  # nombre sin extensión
FIXTURE_FILENAME = "voluntariado_fixture.json"


def _try_loaddata(arg) -> tuple[bool, str | None]:
    try:
        call_command("loaddata", arg, verbosity=0)
        return True, None
    except CommandError as e:
        return False, str(e)


def _seed_voluntariado_once(sender, **kwargs):
    with connection.cursor() as cur, transaction.atomic():
        # Asegura tabla de control
        cur.execute("CREATE TABLE IF NOT EXISTS seed_run(tag TEXT PRIMARY KEY)")

        # ¿Ya corrimos esta versión?
        cur.execute("SELECT 1 FROM seed_run WHERE tag=%s", [SEED_TAG])
        if cur.fetchone():
            print(f"[seed_voluntariado] Ya corrido {SEED_TAG}, no se recarga")
            return

        loaded = False
        err = None

        # 1) Intento estándar: por nombre (Django buscará en app/fixtures y FIXTURE_DIRS)
        ok, err = _try_loaddata(FIXTURE_BASENAME)
        if ok:
            print(f"[seed_voluntariado] Cargado por nombre: {FIXTURE_BASENAME}")
            loaded = True
        else:
            print(
                f"[seed_voluntariado] No se encontró por nombre ({FIXTURE_BASENAME}). Probando rutas…"
            )

            # 2) Búsqueda en rutas conocidas
            seeds_dir = Path(__file__).resolve().parent  # participa/seeds
            app_dir = seeds_dir.parent  # participa
            candidate_dirs = [
                app_dir / "fixtures",  # participa/fixtures
                seeds_dir / "fixtures",  # participa/seeds/fixtures
            ]

            # FIXTURE_DIRS de settings (si existen)
            try:
                for p in getattr(settings, "FIXTURE_DIRS", []):
                    candidate_dirs.append(Path(p))
            except Exception:
                pass

            # Evita duplicados manteniendo orden
            seen = set()
            ordered_candidates = []
            for d in candidate_dirs:
                if d not in seen:
                    ordered_candidates.append(d)
                    seen.add(d)

            # Recorre candidatos
            for d in ordered_candidates:
                path = d / FIXTURE_FILENAME
                if path.exists():
                    ok, err = _try_loaddata(str(path))
                    if ok:
                        print(f"[seed_voluntariado] Cargado fixture: {path}")
                        loaded = True
                        break
                    else:
                        print(f"[seed_voluntariado] ERROR cargando {path.name}: {err}")

            if not loaded:
                # Log informativo de dónde se buscó
                print("[seed_voluntariado] No encontré la fixture en:")
                for d in ordered_candidates:
                    print(f"  - {d}")
                if err:
                    print(f"[seed_voluntariado] Último error: {err}")

        # 3) Marca solo si efectivamente cargó
        if loaded:
            cur.execute("INSERT INTO seed_run(tag) VALUES(%s)", [SEED_TAG])
            print(f"[seed_voluntariado] Marcado {SEED_TAG}")
        else:
            print("[seed_voluntariado] No se cargó nada. NO marco el SEED_TAG.")
