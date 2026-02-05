# donaciones/migrations/0005_remove_donacionsection_progreso.py
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "donaciones",
            "0004_alter_donacionsection_progreso",
        ),  # <- ESTA debe ser la 0004
    ]

    operations = [
        migrations.RemoveField(
            model_name="donacionsection",
            name="progreso",
        ),
        # ... (lo que ya tengas)
    ]
