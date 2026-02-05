# core/utils/seed_media.py
from pathlib import Path
from shutil import copy2
from django.conf import settings

DEFAULT_PAIRS = [
    (Path("eventos/static/images"), Path("images")),
    # NOSOTROS (coinciden con upload_to de los modelos)
    (Path("nosotros/static/nosotros/images"), Path("nosotros")),
    (
        Path("nosotros/static/nosotros/images/pilares/ecologia"),
        Path("nosotros/headers"),
    ),
    (
        Path("nosotros/static/nosotros/images/pilares/ecologia"),
        Path("nosotros/pilares/hero"),
    ),
    (
        Path("nosotros/static/nosotros/images/pilares/economia-comunitaria"),
        Path("nosotros/pilares/hero"),
    ),
    (
        Path("nosotros/static/nosotros/images/pilares/economia-comunitaria"),
        Path("nosotros/pilares/hero"),
    ),
    (
        Path("nosotros/static/nosotros/images/pilares/sociocultural"),
        Path("nosotros/headers"),
    ),
    (
        Path("nosotros/static/nosotros/images/pilares/sociocultural"),
        Path("nosotros/pilares/hero"),
    ),
    (Path("nosotros/static/nosotros/images/pilares"), Path("nosotros/pilares/hero")),
    (Path("nosotros/static/nosotros/images/pilares"), Path("nosotros/headers")),
    (Path("nosotros/static/nosotros/images/pilares"), Path("nosotros/sections/hero")),
    (Path("nosotros/static/nosotros/images"), Path("nosotros/headers")),
    (Path("nosotros/static/nosotros/images"), Path("nosotros/sections/hero")),
    (
        Path("nosotros/static/nosotros/images/pilares/ecologia"),
        Path("nosotros/images/pilares/ecologia"),
    ),
    # INICIO (coinciden con upload_to de los modelos)
    (Path("inicio/static/inicio/hero"), Path("inicio/hero")),
    (Path("inicio/static/inicio/icons"), Path("inicio/icons")),
    (Path("inicio/static/inicio/proyectos"), Path("inicio/proyectos")),
    (Path("inicio/static/inicio/productos"), Path("inicio/productos")),
    (
        Path("inicio/static/images/galerias/galerias_ultimos_eventos/portadas"),
        Path("inicio/galerias/portadas"),
    ),
    (
        Path("inicio/static/images/galerias/galerias_ultimos_eventos/items"),
        Path("inicio/galerias/items"),
    ),
    (Path("inicio/static/images/proyectos"), Path("inicio/galerias/portadas")),
    (Path("inicio/static/images/proyectos/items"), Path("inicio/galerias/items")),
    (
        Path("participa/static/participa/images/estancias/casas"),
        Path("estancias/portadas"),
    ),
    (
        Path("participa/static/participa/images/estancias/casas"),
        Path("estancias/fotos"),
    ),
    (Path("participa/static/participa/images/estancias"), Path("participa/headers")),
    (Path("inicio/static/images/galerias/casas"), Path("participa/instagram")),
    (Path("tienda/static/images"), Path("productos/portadas")),
    (
        Path("cooperaciones/static/images/coops/fotos/"),
        Path("coops/fotos/red-agroecologica"),
    ),
    (Path("cooperaciones/static/images/coops/logos/"), Path("coops/logos")),
    (Path("cooperaciones/static/images/coops/portadas/"), Path("coops/portadas")),
    (
        Path("participa/static/participa/images/voluntariado/"),
        Path("participa/voluntariado/hero"),
    ),
    (Path("participa/static/participa/images/"), Path("images")),
    (Path("participa/static/participa/images/"), Path("participa/voluntariado/thumb")),
    (Path("visitas/static/visitas/landing"), Path("visitas/landing")),
    (Path("visitas/static/visitas/portadas"), Path("visitas/inner")),
    (Path("visitas/static/visitas/portadas"), Path("visitas/portadas")),
    (Path("visitas/static/visitas/galeria"), Path("visitas/galeria")),
    (Path("visitas/static/visitas/galeria"), Path("visitas/galeria")),
    (Path("donaciones/static/images/cabezadonaciones.png"), Path("donaciones")),
    (Path("blog/static/blog/header"), Path("blog/header")),
    (Path("blog/static/blog/portadas"), Path("blog/portadas")),
    (Path("blog/static/blog/gallery"), Path("blog/gallery")),
]


def copy_seed_media(pairs=DEFAULT_PAIRS, force=False) -> int:
    base = Path(settings.BASE_DIR)
    media = Path(settings.MEDIA_ROOT)
    media.mkdir(parents=True, exist_ok=True)

    total = 0
    for src_rel, dst_rel in pairs:
        src = base / src_rel
        dst = media / dst_rel
        if not src.exists():
            continue
        dst.mkdir(parents=True, exist_ok=True)
        for f in src.glob("*"):
            if f.is_file():
                target = dst / f.name
                if target.exists() and not force:
                    continue
                copy2(f, target)
                total += 1
    return total
