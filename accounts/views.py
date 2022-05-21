from django.shortcuts import render

# Create your views here.

# builtin: UserCreationForm para registro
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
=======
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
>>>>>>> 856d9a216734950c926e57902d9746624bca4538
from .forms import SignUpForm, VacunasAnterioresForm, ElegirCentroForm
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic import RedirectView
"""
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    # reverse_lazy es para redirigir el usuario a la pagina de login luego de registrarse
    # reverse_lazy en vez de reverse porque para todas las vistas basadas en clases genericas no se cargan las urls
    # y lazy indica esperar a que se carguen
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
"""


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.paciente.dni = form.cleaned_data.get('dni')
        user.paciente.first_name = form.cleaned_data.get('first_name')
        user.paciente.last_name = form.cleaned_data.get('last_name')
        user.paciente.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    # descomentar esto es poco informativo para el user
    # else:
    #    form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

<<<<<<< HEAD
def vacunasAnteriores_view(request):
    form = VacunasAnterioresForm(request.POST)
    if form.is_valid():
        vacun = form.save(commit = False)
        vacun.user = request.user
        vacun.save()

    return render(request, 'vacunas_anteriores.html', {'form' : form})

def userinfo_view(request):
    return render(request, 'userinfo.html')

=======
def userinfo_view(request):
    return render(request, 'userinfo.html')



def vacunasAnteriores_view(request):
   form = VacunasAnterioresForm(request.POST)
   if form.is_valid():
       vacun = form.save(commit = False)
       vacun.fiebre_amarilla = form.cleaned_data.get('fiebre_amarilla')
       vacun.gripe = form.cleaned_data.get('gripe')
       vacun.covid_1 = form.cleaned_data.get('covid_1')
       vacun.covid_2 = form.cleaned_data.get('covid_2')
       vacun.user = request.user
       vacun.save()

   return render(request, 'vacunas_anteriores.html', {'form' : form})

>>>>>>> 856d9a216734950c926e57902d9746624bca4538
def cambiarContraseña_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Tu contraseña se cambió correctamente')
            return redirect('home')
        else:
            messages.error(request, 'Ocurrió un error, intente nuevamente.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cambiar_contrasena.html', {'form': form})

def elegirCentro_view(request):
     form = ElegirCentroForm(request.POST)
     if form.is_valid():
        centro = form.save(commit = False)
        centro.centros = form.cleaned_data.get('centros')
        centro.user = request.user
        centro.save()

     return render(request, 'elegir_centro.html', {'form' : form})


<<<<<<< HEAD
=======

>>>>>>> 856d9a216734950c926e57902d9746624bca4538

