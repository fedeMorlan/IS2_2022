# Generated by Django 4.0.4 on 2022-05-22 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0013_remove_paciente_centro_vacunacion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacunasanteriores',
            name='id',
        ),
        migrations.AlterField(
            model_name='vacunasanteriores',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
