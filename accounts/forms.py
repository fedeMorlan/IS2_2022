from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
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
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)
