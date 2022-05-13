from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# tal como se indica en https://dev.to/thepylot/create-advanced-user-sign-up-view-in-django-step-by-step-k9m

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dni = models.CharField(max_length=8, help_text='DNI')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    bio = models.TextField()
    # el password lo maneja otro api, por ahi esta bueno para que no figure el texto en la bd

    def __str__(self):
        return self.user.username


class CentroDeVacunacion(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True)
    direccion = models.CharField(max_length=100)


class Vacuna(models.Model):
    nombrevacuna = models.CharField(max_length=100, primary_key=True)
    numero_de_lote = models.IntegerField
    # YYYY-MM-DD
    fecha_vencimiento = models.DateField


class Aplicacion(models.Model):
    # ya es primary key por ser AutoField
    id_aplicacion = models.AutoField
    nombrevacuna = models.CharField(max_length=100)
    fecha_de_aplicacion = models.DateField
    # no estoy seguro de como funciona el ForeignKey
    id_paciente = models.ForeignKey
    id_vacunador = models.ForeignKey


class VacunasAnteriores(models.Model):
    id_paciente = models.ForeignKey
    fiebre_amarilla = models.BooleanField
    gripe = models.BooleanField
    covid_1 = models.BooleanField
    covid_2 = models.BooleanField


class Pacientevacunas(models.Model):
    id_pacientevacunas = models.AutoField
    nombreusuario = models.ForeignKey
    nombre_vacuna = models.ForeignKey


class Turno(models.Model):
    id_turno = models.AutoField
    nombreusuario = models.ForeignKey
    hora = models.TimeField
    fecha = models.DateField


class Vacunador(models.Model):
    nombreusuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dni = models.CharField(max_length=8)
    email = models.EmailField(max_length=150)
    # password


class TrabajaEn(models.Model):
    id_trabaja_en = models.AutoField
    nombreusuario = models.ForeignKey
    nombrecentro = models.ForeignKey


class Dueno(models.Model):
    nombreusuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dni = models.CharField(max_length=8)
    email = models.EmailField(max_length=150)
    # password


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Paciente.objects.create(user=instance)
    instance.paciente.save()
    # instance.profile.save()
# Create your models here.
