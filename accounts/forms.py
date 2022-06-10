from enum import unique
from tkinter import HIDDEN
from tkinter.tix import Form
from urllib import request
from urllib.request import Request
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from accounts.models import Paciente, VacunasAnteriores, CentroDeVacunacion


class SignUpForm(UserCreationForm):
    dni = forms.CharField(max_length=8, help_text='DNI sin puntos', label='DNI')
    first_name = forms.CharField(max_length=100, help_text='Nombre', label='Nombre')
    last_name = forms.CharField(max_length=100, help_text='Apellido', label='Apellido')
    email = forms.EmailField(max_length=150, help_text='Email', label='Email')
    username = forms.CharField(max_length=150, help_text='Nombre de Usuario', label='Nombre de Usuario')
    edad = forms.IntegerField(label='Edad', min_value=0, max_value=120)
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Confirmación de contraseña",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Ingresar la misma contraseña que antes, para verificación.",
    )

    # def clean_email(self):
    #    email = self.cleaned_data.get('email')
    #    if User.objects.filter(email=email).exists():
    #        raise forms.ValidationError("Este email ya está registrado")
    #    else: return email

    class Meta:
        model = User
        fields = ('username', 'dni', 'edad', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)


class VacunasAnterioresForm(ModelForm):
    opciones = [('True', 'Si'), ('False', 'No')]
    fiebre_amarilla = forms.ChoiceField(widget=forms.RadioSelect, choices=opciones, label='Fiebre Amarilla',
                                        help_text="En los ultimos 10 años")
    gripe = forms.ChoiceField(widget=forms.RadioSelect, choices=opciones, label='Gripe ',
                              help_text="En los ultimos 12 meses")
    covid_1 = forms.ChoiceField(widget=forms.RadioSelect, choices=opciones, label='Covid - dosis 1')
    covid_2 = forms.ChoiceField(widget=forms.RadioSelect, choices=opciones, label='Covid - dosis 2')

    class Meta:
        model = VacunasAnteriores
        fields = ('fiebre_amarilla', 'gripe', 'covid_1', 'covid_2')


class ElegirCentroForm(ModelForm):
    opciones = [('Comedor Universitario', 'Comedor Universitario'), ('Hipodromo', 'Hipodromo'), ('Bosque', 'Bosque')]
    nombre = forms.ChoiceField(widget=forms.RadioSelect, choices=opciones, label='Elegi tu centro')

    class Meta:
        model = CentroDeVacunacion
        fields = ('nombre',)


class ModificarDatosForm(ModelForm):
    if User.is_authenticated:
        dni = forms.CharField(max_length=8, label='DNI')
        first_name = forms.CharField(max_length=100, label='Nombre')
        last_name = forms.CharField(max_length=100, label='Apellido')
        email = forms.EmailField(max_length=150, label='Email')
        edad = forms.IntegerField(label='Edad', min_value=0, max_value=120, help_text='entre 0 y 120')
        #username = forms.CharField(max_length=150, help_text='debe ser único', label='Nombre de Usuario')

       #def clean_email(self):
       #    email = self.cleaned_data.get('email')
       #    if User.objects.filter(email=email).exists():
       #        raise forms.ValidationError("Este email ya está registrado")
       #    else: return email
       
    else:
        pass

    class Meta:
        model = Paciente
        fields = ( 'dni', 'first_name', 'last_name','edad', 'email')

class ModificarDatosForm2(ModelForm):
    if User.is_authenticated:
        username = forms.CharField(max_length=150, help_text='debe ser único', label='Nombre de Usuario')
    else:
        pass

    class Meta:
        model = User
        fields = ('username',)

class validarIdentidadRenaperForm(forms.Form):
    if User.is_authenticated:
        frente = forms.ImageField(required=True, help_text='Imagen del frente de su DNI')
        dorso = forms.ImageField(required=True, help_text='Imagen del dorso de su DNI')
        #validado_renaper = forms.BooleanField()
    else: 
        pass 

   #class Meta:
   #    model = Paciente
   #    fields = ('validado_renaper',)