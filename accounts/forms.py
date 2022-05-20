from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.forms import UserCreationForm

from accounts.models import VacunasAnteriores




class SignUpForm(UserCreationForm):
    dni = forms.CharField(max_length=8, help_text='DNI sin puntos', label='DNI')
    first_name = forms.CharField(max_length=100, help_text='Nombre', label='Nombre')
    last_name = forms.CharField(max_length=100, help_text='Apellido', label='Apellido')
    sexo = forms.CharField(max_length=2, help_text='Femenino(F) Masculino (M) No Binario (NB)',label='Sexo')
    fecha_nacimiento = forms.DateField(label='Fecha de nacimiento')
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
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado")
    
    class Meta:
        model = User
        fields = ('username', 'dni', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)

class VacunasAnterioresForm(ModelForm):
    opciones = [('True', 'Si'), ('False', 'No')]
    fiebre_amarilla = forms.ChoiceField(widget = forms.RadioSelect, choices = opciones, label = 'Fiebre Amarilla')
    gripe = forms.ChoiceField(widget = forms.RadioSelect, choices = opciones, label = 'Gripe ',)
    covid_1 = forms.ChoiceField(widget = forms.RadioSelect, choices = opciones, label = 'Covid - dosis 1')
    covid_2 = forms.ChoiceField(widget = forms.RadioSelect, choices = opciones, label = 'Covid - dosis 2')
    class Meta:
        model = VacunasAnteriores
        fields = ('fiebre_amarilla', 'gripe', 'covid_1', 'covid_2')