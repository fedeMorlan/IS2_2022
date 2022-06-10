from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.deletion import *


# tal como se indica en https://dev.to/thepylot/create-advanced-user-sign-up-view-in-django-step-by-step-k9m

class CentroDeVacunacion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)


class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dni = models.CharField(max_length=8, help_text='DNI')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    bio = models.TextField()
    edad = models.IntegerField(default=0)
    validado_renaper = models.BooleanField(default=False)
    # centro_vacunacion = models.ForeignKey(CentroDeVacunacion, on_delete=models.DO_NOTHING)
    # sexos=[('F','Femenino'),('M','Masculino'),('NB','No Binario'),('NC','No Contesta')]
    # sexo = models.CharField(max_length=2, choices=sexos,default='NC')

    # el password lo maneja otro api, por ahi esta bueno para que no figure el texto en la bd

    def __str__(self):
        return self.user.username


class Vacuna(models.Model):
    nombrevacuna = models.CharField(max_length=100, primary_key=True)
    numero_de_lote = models.IntegerField
    # YYYY-MM-DD
    fecha_vencimiento = models.DateField


class Vacunador(models.Model):
    nombreusuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dni = models.CharField(max_length=8)
    email = models.EmailField(max_length=150)
    # password


class Aplicacion(models.Model):
    # ya es primary key por ser AutoField
    id_aplicacion = models.AutoField
    nombrevacuna = models.CharField(max_length=100)
    fecha_de_aplicacion = models.DateField
    # no estoy seguro de como funciona el ForeignKey
    id_paciente = models.ForeignKey(Paciente, null=False, blank=False, on_delete=models.CASCADE)
    id_vacunador = models.ForeignKey(Vacunador, null=False, blank=False, on_delete=models.CASCADE)


class VacunasAnteriores(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    fiebre_amarilla = models.BooleanField(null=True)
    gripe = models.BooleanField(null=True)
    covid_1 = models.BooleanField(null=True)
    covid_2 = models.BooleanField(null=True)

    def __str__(self):
        tupla = ()
        if (self.fiebre_amarilla): tupla += ("fiebre amarilla",)
        if (self.gripe): tupla += ("gripe",)
        if (self.covid_1): tupla += ("covid dosis 1",)
        if (self.covid_2): tupla += ("covid dosis 2",)
        vax = ", ".join(tupla)
        if len(tupla) == 0:
            vax = "No registra vacunas aplicadas"
        return vax


class Pacientevacunas(models.Model):
    id_pacientevacunas = models.AutoField
    nombreusuario = models.ForeignKey(Paciente, null=False, blank=False, on_delete=models.CASCADE)
    nombre_vacuna = models.ForeignKey(Vacuna, null=False, blank=False, on_delete=models.CASCADE)


class Turno(models.Model):
    id_turno = models.AutoField
    nombreusuario = models.ForeignKey(Paciente, null=False, blank=False, on_delete=models.CASCADE)
    centro = models.ForeignKey(CentroDeVacunacion,null=False,on_delete=models.CASCADE, default=1)
    hora = models.TimeField
    fecha = models.DateField


# class TrabajaEn(models.Model):
#    id_trabaja_en = models.AutoField
#    nombreusuario = models.ForeignKey(Vacunador, null=False, blank=False, on_delete=models.CASCADE)
#    #nombrecentro = models.ForeignKey(CentroDeVacunacion, null=False, blank=False, on_delete=models.CASCADE)


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
