# Generated by Django 4.0.4 on 2022-06-02 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_paciente_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='edad',
            field=models.IntegerField(default=0),
        ),
    ]