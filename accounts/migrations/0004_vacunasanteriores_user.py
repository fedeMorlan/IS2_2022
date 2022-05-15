# Generated by Django 4.0.4 on 2022-05-15 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_remove_vacunasanteriores_nombre_vacuna'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacunasanteriores',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
