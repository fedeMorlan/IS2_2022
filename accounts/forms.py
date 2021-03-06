from asyncore import write
from enum import unique
from tkinter import HIDDEN
from tkinter.tix import Form
from urllib import request
from urllib.request import Request
import datetime
from xml.dom import ValidationErr
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.forms import ModelForm, ValidationError
from accounts.models import Paciente, VacunasAnteriores, CentroDeVacunacion, Turno, TurnoSlot, HoraTurno, Vacuna, \
    VacunasAnteriores, CentroDeVacunacion, Aplicacion


class DateInput(forms.DateInput):
    input_type = 'date'
    input_min = '2020-01-01'
    input_max = '2021-01-01'


class SignUpForm(UserCreationForm):
    dni = forms.CharField(max_length=8, help_text='DNI sin puntos', label='DNI')
    first_name = forms.CharField(max_length=100, help_text='Nombre', label='Nombre')
    last_name = forms.CharField(max_length=100, help_text='Apellido', label='Apellido')
    email = forms.EmailField(max_length=150, help_text='Email', label='Email')
    username = forms.CharField(max_length=150, help_text='Nombre de Usuario', label='Nombre de Usuario')
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
        fields = ('username', 'dni', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)


class SignUpForm2(ModelForm):
    nacimiento = forms.DateInput()
    opciones = [('True', 'Si'), ('False', 'No')]
    comorbilidad = forms.ChoiceField(widget=forms.RadioSelect, choices=opciones, label='Comorbilidades')

    class Meta:
        model = Paciente
        fields = ('nacimiento', 'comorbilidad',)
        widgets = {
            'nacimiento': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'min': '1920-01-01',
                                                                      'max': '2022-06-13', 'value': '2000-01-25'})
        }


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
    # opciones = [(CentroDeVacunacion.objects.get(pk='Bosque'), 'Bosque'),
    #            (CentroDeVacunacion.objects.get(pk='Comedor Universitario'), 'Comedor Universitario'),
    #            (CentroDeVacunacion.objects.get(pk='Hipodromo'), 'Hipodromo')]
    # nombre = forms.ChoiceField(widget=forms.RadioSelect, choices=opciones, label='Elegi tu centro')

    class Meta:
        model = Paciente
        fields = ('centro_vacunacion',)


class ModificarDatosForm(ModelForm):
    if User.is_authenticated:
        dni = forms.CharField(max_length=8, label='DNI')
        first_name = forms.CharField(max_length=100, label='Nombre')
        last_name = forms.CharField(max_length=100, label='Apellido')
        email = forms.EmailField(max_length=150, label='Email')
        # nacimiento = forms.DateInput()
        opciones = [('True', 'Si'), ('False', 'No')]
        comorbilidad = forms.ChoiceField(widget=forms.RadioSelect, choices=opciones, label='Comorbilidades')
        # username = forms.CharField(max_length=150, help_text='debe ser único', label='Nombre de Usuario')

    # def clean_email(self):
    #    email = self.cleaned_data.get('email')
    #    if User.objects.filter(email=email).exists():
    #        raise forms.ValidationError("Este email ya está registrado")
    #    else: return email

    else:
        pass

    class Meta():
        model = Paciente
        fields = ('dni', 'first_name', 'last_name', 'nacimiento', 'email', 'comorbilidad')
        widgets = {
            'nacimiento': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'min': '1920-01-01',
                                                                      'max': '2022-06-13', })
        }


class ModificarDatosForm2(ModelForm):
    if User.is_authenticated:
        username = forms.CharField(max_length=150, help_text='debe ser único', label='Nombre de Usuario')
    else:
        pass

    class Meta:
        model = User
        fields = ('username',)


class validarIdentidadRenaperForm(ModelForm):
    if User.is_authenticated:
        frente = forms.ImageField(help_text='Imagen del frente de su DNI')
        dorso = forms.ImageField(help_text='Imagen del dorso de su DNI')
        # validado_renaper = forms.BooleanField()
    else:
        pass

    class Meta:
        model = Paciente
        fields = ()


class registrarAplicacionForm(ModelForm):
    nombrevacuna = forms.ModelChoiceField(label='Nombre de la vacuna', queryset=
    Vacuna.objects.all())
    fecha_de_aplicacion = forms.DateField(label='Fecha de la aplicación', widget=forms.widgets.DateInput(
        attrs={'type': 'date'}
    ))
    numero_de_lote = forms.IntegerField(label='Lote')
    id_paciente = forms.ModelChoiceField(label='usuario del paciente', queryset=
    Paciente.objects.all())

    # widget=autocomplete.ModelSelect2(url='paciente-autocomplete'))
    class Meta:
        model = Aplicacion
        fields = ('nombrevacuna', 'fecha_de_aplicacion', 'numero_de_lote', 'id_paciente')


class SolicitarTurnoForm(ModelForm):
    fecha = forms.DateInput()

    class Meta:
        model = TurnoSlot
        fields = ('fecha',)
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'min': '2022-06-13', 'max': '2024-01-01'})
        }


class SolicitarTurnoForm2(ModelForm):
    # se requiere hacer un inicializador del form que pueda tomar al usuario como parametro
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(SolicitarTurnoForm2, self).__init__(*args, **kwargs)

        # se genera dinamicamente el queryset de las vacunas segun las vacunas anteriores del paciente
        vacunas_anteriores_paciente = VacunasAnteriores.objects.get(user=self.user)
        # no se puede elegir turno de fiebre amarilla porque es en el momento
        elecciones = Vacuna.objects.exclude(nombrevacuna='fiebre amarilla')
        # no se debe poder elegir COVID 2 si el paciente no tiene COVID 1 o si ya se dio la 2
        if not vacunas_anteriores_paciente.covid_1 or vacunas_anteriores_paciente.covid_2:
            elecciones = elecciones.exclude(nombrevacuna='COVID 2')
        # no se deben poder elegir vacunas que el paciente ya tiene
        if vacunas_anteriores_paciente.covid_1:
            elecciones = elecciones.exclude(nombrevacuna='COVID 1')
        # dejamos que la vacuna de la gripe se pueda dar varias veces

        self.fields['nombrevacuna'].queryset = elecciones

    # campo del form, se asigna queryset None para que tome dinamicamente del constructor
    nombrevacuna = forms.ModelMultipleChoiceField(label='Vacuna', queryset=None, required=True,
                                                  widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Turno
        labels = {
            "horaturnoID": "Horario",
        }
        fields = ('nombrevacuna', 'horaturnoID',)


class CancelarTurnoForm(ModelForm):
    class Meta:
        model = Turno
        fields = ()


class CustomEmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email2 = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email2).exists():
            raise ValidationError("No hay usuarios registrados con este email")

        return email2


class TurnosDelDiaPorCentroForm(ModelForm):
    centro = forms.ModelChoiceField(queryset=CentroDeVacunacion.objects.all())
    class Meta:
        model = CentroDeVacunacion
        fields = ('centro',)


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email no registrado")
        return email

class BuscarPacienteForm(ModelForm):
    username = forms.CharField(max_length=150, label='Nombre o apellido')
    class Meta:
        model = Paciente
        fields = ('username',)

class BuscarVacunadorForm(ModelForm):
    username = forms.CharField(max_length=150, label='Nombre o apellido')
    class Meta:
        model = Paciente
        fields = ('username',)
