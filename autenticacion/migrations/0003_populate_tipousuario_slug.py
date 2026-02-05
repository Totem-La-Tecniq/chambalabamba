from django.db import migrations
from django.utils.text import slugify


def fill_slugs(apps, schema_editor):
    TipoUsuario = apps.get_model("autenticacion", "TipoUsuario")
    for tu in TipoUsuario.objects.all():
        if not getattr(tu, "slug", None):
            base = slugify(tu.nombre) or "tipo"
            slug = base
            i = 1
            while TipoUsuario.objects.filter(slug=slug).exclude(pk=tu.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            tu.slug = slug
            tu.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [("autenticacion", "0002_add_tipousuario_slug")]

    operations = [
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
    ]
