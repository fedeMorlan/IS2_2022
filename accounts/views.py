from django.shortcuts import render

# Create your views here.

# builtin: UserCreationForm para registro
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import CentroDeVacunacion, Paciente, VacunasAnteriores
from .forms import ModificarDatosForm2, SignUpForm, VacunasAnterioresForm, ElegirCentroForm, ModificarDatosForm
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

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
        user.paciente.refresh_from_db()
        user.paciente.dni = form.cleaned_data.get('dni')
        user.paciente.first_name = form.cleaned_data.get('first_name')
        user.paciente.last_name = form.cleaned_data.get('last_name')
        user.paciente.email = form.cleaned_data.get('email')
        user.paciente.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    # descomentar esto es poco informativo para el user
    # else:
    #    form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def userinfo_view(request):
    try:
        centroElegido = CentroDeVacunacion.objects.get(user__id=request.user.id)
        request.centro = centroElegido.nombre
        vacunas = VacunasAnteriores.objects.get(user__id=request.user.id)
        request.vacunas = vacunas.__str__()
    except:
        pass
    return render(request, 'userinfo.html')


def vacunasAnteriores_view(request):
    form = VacunasAnterioresForm(request.POST)
    if form.is_valid():
        vacun = form.save(commit=False)
        vacun.fiebre_amarilla = form.cleaned_data.get('fiebre_amarilla')
        vacun.gripe = form.cleaned_data.get('gripe')
        vacun.covid_1 = form.cleaned_data.get('covid_1')
        vacun.covid_2 = form.cleaned_data.get('covid_2')
        vacun.user = request.user
        vacun.save()
        return redirect('userinfo')

    return render(request, 'vacunas_anteriores.html', {'form': form})


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
        centro = form.save(commit=False)
        centro.nombre = form.cleaned_data.get('nombre')
        centro.user = request.user
        centro.save()
        return redirect('userinfo')

    return render(request, 'elegir_centro.html', {'form': form})


@login_required
def modificarDatos_view(request):
    user = request.user.id
    paciente = Paciente.objects.get(user__id=user)
    user_info = User.objects.get(id=user)
    if request.method == 'POST':
        form = ModificarDatosForm(request.POST, request.FILES, instance=paciente)
        form2 = ModificarDatosForm2(request.POST, request.FILES,instance = user_info)
        if form.is_valid() and form2.is_valid():
            user_info.paciente.dni = form.cleaned_data.get('dni')
            user_info.paciente.email = form.cleaned_data.get('email')
            user_info.email = user_info.paciente.email
            user_info.paciente.first_name = form.cleaned_data.get('first_name')
            user_info.paciente.last_name = form.cleaned_data.get('last_name')
            user_info.paciente.edad = form.cleaned_data.get('edad')
            user_info.username = form2.cleaned_data.get('username')
            paciente.save()
            try:
                user_info.save()
            except:
                pass
            return redirect('userinfo')
    else:
        form = ModificarDatosForm(instance=paciente)
        form2 = ModificarDatosForm2(instance = user_info)

    return render(request, 'modificar_datos.html', {'form': form, 'form2':form2})
