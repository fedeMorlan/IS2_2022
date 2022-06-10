# Generated by Django 4.0.4 on 2022-06-10 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CentroDeVacunacion',
            fields=[
                ('nombre', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('direccion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Dueno',
            fields=[
                ('nombreusuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('dni', models.CharField(max_length=8)),
                ('email', models.EmailField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('dni', models.CharField(help_text='DNI', max_length=8)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=150)),
                ('bio', models.TextField()),
                ('edad', models.IntegerField(default=0)),
                ('validado_renaper', models.BooleanField(default=False)),
                ('centro_vacunacion', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.centrodevacunacion')),
            ],
        ),
        migrations.CreateModel(
            name='TurnoSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechayhora', models.DateTimeField()),
                ('cupo', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Vacuna',
            fields=[
                ('nombrevacuna', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Vacunador',
            fields=[
                ('nombreusuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('dni', models.CharField(max_length=8)),
                ('email', models.EmailField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='VacunasAnteriores',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('fiebre_amarilla', models.BooleanField(null=True)),
                ('gripe', models.BooleanField(null=True)),
                ('covid_1', models.BooleanField(null=True)),
                ('covid_2', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id_turno', models.AutoField(primary_key=True, serialize=False)),
                ('centro', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.centrodevacunacion')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.paciente')),
                ('turnoSlotID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.turnoslot')),
                ('vacunador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.vacunador')),
            ],
        ),
        migrations.CreateModel(
            name='Aplicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombrevacuna', models.CharField(max_length=100)),
                ('id_paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.paciente')),
                ('id_vacunador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.vacunador')),
            ],
        ),
    ]
