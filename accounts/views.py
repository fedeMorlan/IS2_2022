from django.shortcuts import render

# Create your views here.

# builtin: UserCreationForm para registro
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm, VacunasAnterioresForm
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

def vacunasAnteriores_view(request):
    form = VacunasAnterioresForm(request.POST)
    if form.is_valid():
        vacun = form.save(commit = False)
        vacun.user = request.user
        vacun.save()

    return render(request, 'vacunas_anteriores.html', {'form' : form})




