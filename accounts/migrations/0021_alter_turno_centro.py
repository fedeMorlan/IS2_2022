# Generated by Django 4.0.4 on 2022-06-02 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_alter_turno_centro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='centro',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.centrodevacunacion'),
        ),
    ]
