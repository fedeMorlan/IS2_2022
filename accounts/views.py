from lib2to3.pgen2.pgen import PgenGrammar
from logging import root
from struct import pack
from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import date
# Create your views here.

# builtin: UserCreationForm para registro
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import CentroDeVacunacion, Paciente, VacunasAnteriores, Aplicacion, TurnoSlot, Turno, HoraTurno
from .forms import *
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from dal import autocomplete
from PIL import Image
import glob, io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
from accounts.models import Vacunador


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
    form = SignUpForm(request.POST, request.FILES)
    form2 = SignUpForm2(request.POST, request.FILES)
    if form.is_valid() and form2.is_valid():
        user = form.save()
        #user2 = form2.save(commit=False)
        user.paciente.refresh_from_db()
        user.paciente.dni = form.cleaned_data.get('dni')
        user.paciente.first_name = form.cleaned_data.get('first_name')
        user.paciente.last_name = form.cleaned_data.get('last_name')
        user.paciente.email = form.cleaned_data.get('email')
        user.paciente.nacimiento = form2.cleaned_data['nacimiento']
        user.paciente.comorbilidad = form2.cleaned_data.get('comorbilidad')
        user.save()
        user.paciente.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    # descomentar esto es poco informativo para el user
    #else:
    #    form = SignUpForm(instance=User)
    #    form2 = SignUpForm2(instance=Paciente)
    return render(request, 'signup.html', {'form': form, 'form2': form2})


def userinfo_view(request):
    try:
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
    user = request.user.id
    paciente = Paciente.objects.get(user__id=user)
    user_info = User.objects.get(id=user)
    if request.method == 'POST':
        form = ElegirCentroForm(request.POST, instance=paciente)
        if form.is_valid():
            user_info.paciente.centro_vacunacion = form.cleaned_data.get('nombre')
            paciente.save()
            try:
                user_info.save()
            except:
                pass
            return redirect('userinfo')
    else:
        form = ElegirCentroForm(instance=paciente)

    return render(request, 'elegir_centro.html', {'form': form})


def verVacunasAplicadas_view(request):
    request.data = Aplicacion.objects.filter(id_paciente=request.user.id).values_list('nombrevacuna')
    return render(request, 'vacunas_aplicadas.html')


@login_required
def modificarDatos_view(request):
    user = request.user.id
    paciente = Paciente.objects.get(user__id=user)
    user_info = User.objects.get(id=user)
    if request.method == 'POST':
        form = ModificarDatosForm(request.POST, request.FILES, instance=paciente)
        form2 = ModificarDatosForm2(request.POST, request.FILES, instance=user_info)
        if form.is_valid() and form2.is_valid():
            user_info.paciente.dni = form.cleaned_data.get('dni')
            user_info.paciente.email = form.cleaned_data.get('email')
            user_info.email = user_info.paciente.email
            user_info.paciente.first_name = form.cleaned_data.get('first_name')
            user_info.paciente.last_name = form.cleaned_data.get('last_name')
            user_info.paciente.nacimiento = form.cleaned_data.get('nacimiento')
            user_info.paciente.comorbilidad = form.cleaned_data.get('comorbilidad')
            user_info.username = form2.cleaned_data.get('username')
            paciente.save()
            try:
                user_info.save()
            except:
                pass
            return redirect('userinfo')
    else:
        form = ModificarDatosForm(instance=paciente)
        form2 = ModificarDatosForm2(instance=user_info)

    return render(request, 'modificar_datos.html', {'form': form, 'form2': form2})


@login_required
def validarIdentidadRenaper_view(request):
    user = request.user.id
    paciente = Paciente.objects.get(user__id=user)
    user_info = User.objects.get(id=user)
    if user_info.paciente.validado_renaper:
        return render(request, 'validado.html')
    else:
        if request.method == 'POST':
            form = validarIdentidadRenaperForm(request.POST, request.FILES, instance=paciente)
            if form.is_valid():
                # frente = form.cleaned_data.get('frente')
                # dorso = form.cleaned_data.get('dorso')
                user_info.paciente.validado_renaper = True
                paciente.save()
                try:
                    user_info.save()
                except:
                    pass

                return render(request, 'validado.html')
        else:
            form = validarIdentidadRenaperForm(instance=paciente)
    return render(request, 'validar_identidad.html', {'form': form})


@login_required
def cancelarTurno_view(request):
    user = request.user.id
    paciente = Paciente.objects.get(user__id=user)
    turnos = Turno.objects
    turno_dic = {}
    form = CancelarTurnoForm(request.POST, request.FILES)
    try:
        turno_data = turnos.get(paciente=paciente)
    except:
        pass
    if request.method == 'POST' and form.is_valid():
        turnoActual = turnos.get(paciente=paciente)
        # aumentar la capacidad del turnoslot correspondiente
        tSlotActual = TurnoSlot.objects.get(slotID=turnoActual.turnoSlotID.slotID)
        tSlotActual.cupo -= 1
        tSlotActual.save()
        # eliminar la tupla de la tabla de turnos
        turnos.filter(paciente=paciente).delete()
        return render(request, 'turno_cancelado.html')
    else:
        form = CancelarTurnoForm()
    return render(request, 'cancelar_turno.html', {"turnoActual": turno_data, "form": form})


@login_required
def turnoPendiente_view(request):
    user = request.user.id
    paciente = Paciente.objects.get(user__id=user)
    turnos = Turno.objects
    turno_dic = {}
    try:
        turno_data = turnos.get(paciente=paciente)
        turno_dic = {"turnoActual": turno_data}
    except:
        pass
    return render(request, 'turno_pendiente.html', turno_dic)


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def calcular_dias(fecha):
    hoy = date.today()
    return (fecha - hoy).days

@login_required
def solicitarTurno_view(request):
    user = request.user.id
    paciente = Paciente.objects.get(user__id=user)
    user_info = User.objects.get(id=user)
    # ---------- CASOS QUE NO PUEDEN PEDIR TURNO --------------
    # si no esta validado en renaper
    if not user_info.paciente.validado_renaper:
        return render(request, 'no_validado.html')
    # if user_info.paciente.

    # si no tiene vacunas previas cargadas en el sistema
    if not VacunasAnteriores.objects.filter(pk=user).exists():
        return render(request, 'no_vacunasprevias.html')

    turnos = TurnoSlot.objects
    turnos2 = Turno.objects
    horas = HoraTurno.objects
    # si ya solicito un turno
    if turnos2.filter(paciente=paciente).exists():
        turno_data = turnos2.get(paciente=paciente)
        # print('DEBUG: ' + str(turno_data))
        turno_dic = {"turnoActual": turno_data, "previo": "ok"}
        return render(request, 'turno_solicitado.html', turno_dic)

    # ----------- PEDIR TURNO --------------------
    # elegir fecha y hora de turno
    form = SolicitarTurnoForm(request.POST, request.FILES)
    form2 = SolicitarTurnoForm2(request.POST, request.FILES)

    if request.method == 'POST' and form.is_valid() and form2.is_valid():
        fechaElegida = form.cleaned_data['fecha']
        horaElegida = form2.cleaned_data.get('horaturnoID').hora
        # print("DEBUG:" + horaElegida)
        horaActual = horas.filter(hora=horaElegida).get()
        # print('DEBUG: entra al loop')

        # definir si la fecha es posible por paciente de riesgo ------
        # creamos un boolean para interrumpir el envio del formulario mas adelante
        ok = True
        if not paciente.comorbilidad and (calculate_age(paciente.nacimiento) < 60):

            if calcular_dias(fechaElegida) <= 30:
                ok = False
                messages.error(request, "Se requiere reservar una fecha posterior a 30 dias por no ser paciente de riesgo")
        else:
            if calcular_dias(fechaElegida) <= 7:
                ok = False
                messages.error(request, "Se requiere reservar una fecha posterior a 7 dias")


        print('DEBUG: dias desde hoy hasta la fecha: ' + str(calcular_dias(fechaElegida)))

        # si la fecha existe
        if turnos.filter(fecha=fechaElegida).exists() and ok:
            # print('DEBUG: existe en la bd')
            turnoSlotActual = turnos.get(fecha=fechaElegida)
            # si hay cupo disponible
            if turnoSlotActual.cupo < 5:
                # print('DEBUG: hay cupo')
                # incrementar el contador y guardar turno
                turnoSlotActual.cupo += 1
                turnoSlotActual.save()
                turno = Turno(paciente=user_info.paciente, turnoSlotID=turnoSlotActual,
                              centro=user_info.paciente.centro_vacunacion, horaturnoID=horaActual)
                turno.save()
                turno_data = turnos2.get(paciente=paciente)
                # print('DEBUG: ' + str(turno_data))
                turno_dic = {"turnoActual": turno_data}
                return render(request, 'turno_solicitado.html', turno_dic)
            # si no hay cupo
            else:
                # mensaje que indica que no hay cupo
                messages.error(request, "No hay mas turnos disponibles en este horario")

        # si la fecha no existe
        elif ok:
            # print('DEBUG: creando una entrada para el slot elegido')
            turnoSlotActual = TurnoSlot(fecha=fechaElegida, cupo=1, horaID=horaActual)
            turnoSlotActual.save()
            turno = Turno(paciente=user_info.paciente, turnoSlotID=turnoSlotActual,
                          centro=user_info.paciente.centro_vacunacion, horaturnoID=horaActual)
            turno.save()
            # crear fecha y guardar turno
            turno_data = turnos2.get(paciente=paciente)
            # print('DEBUG: ' + str(turno_data))
            turno_dic = {"turnoActual": turno_data}
            return render(request, 'turno_solicitado.html', turno_dic)
    else:
        # print('DEBUG: form is not valid')
        form = SolicitarTurnoForm()
        form2 = SolicitarTurnoForm2()


    # FALTA: enviar mail de turno
    return render(request, 'solicitar_turno.html', {'form': form, 'form2': form2})


def borrarTurno(turno):
    # aumentar la capacidad del turnoslot correspondiente
    tSlotActual = TurnoSlot.objects.get(slotID=turno.turnoSlotID.slotID)
    # print("DEBUG: turnoSlot a restar: " + str(tSlotActual))
    tSlotActual.cupo -= 1
    tSlotActual.save()
    # eliminar la tupla de la tabla de turnos
    turno.delete()
    return

@login_required
def modificarTurno_view(request):

    user = request.user.id
    paciente = Paciente.objects.get(user__id=user)
    user_info = User.objects.get(id=user)
    form = SolicitarTurnoForm(request.POST, request.FILES)
    form2 = SolicitarTurnoForm2(request.POST, request.FILES)
    turnos = TurnoSlot.objects
    turnos2 = Turno.objects
    horas = HoraTurno.objects
    if request.method == 'POST' and form.is_valid() and form2.is_valid():
        fechaElegida = form.cleaned_data['fecha']
        horaElegida = form2.cleaned_data.get('horaturnoID').hora
        # print("DEBUG:" + horaElegida)
        horaActual = horas.filter(hora=horaElegida).get()
        # print('DEBUG: entra al loop')

        # definir si la fecha es posible por paciente de riesgo ------
        # creamos un boolean para interrumpir el envio del formulario mas adelante
        ok = True
        if not paciente.comorbilidad and (calculate_age(paciente.nacimiento) < 60):

            if calcular_dias(fechaElegida) <= 30:
                ok = False
                messages.error(request,
                               "Se requiere reservar una fecha posterior a 30 dias por no ser paciente de riesgo")
        else:
            if calcular_dias(fechaElegida) <= 7:
                ok = False
                messages.error(request, "Se requiere reservar una fecha posterior a 7 dias")

        print('DEBUG: dias desde hoy hasta la fecha: ' + str(calcular_dias(fechaElegida)))

        # si la fecha existe
        if turnos.filter(fecha=fechaElegida).exists() and ok:
            # print('DEBUG: existe en la bd')
            turnoSlotActual = turnos.get(fecha=fechaElegida)
            # si hay cupo disponible
            if turnoSlotActual.cupo < 5:
                # print('DEBUG: hay cupo')

                # eliminar el anterior y actualizar el slot correspondiente
                borrarTurno(turnos2.get(paciente=paciente))

                # incrementar el contador y guardar turno
                turnoSlotActual.refresh_from_db()
                turnoSlotActual.cupo += 1
                turnoSlotActual.save()
                turno = Turno(paciente=user_info.paciente, turnoSlotID=turnoSlotActual,
                              centro=user_info.paciente.centro_vacunacion, horaturnoID=horaActual)
                turno.save()

                # print('DEBUG: ' + str(turno_data))
                turno_dic = {"turnoActual": turno}
                return render(request, 'turno_solicitado.html', turno_dic)
            # si no hay cupo
            else:
                # mensaje que indica que no hay cupo
                messages.error(request, "No hay mas turnos disponibles en este horario")

        # si la fecha no existe
        elif ok:
            # eliminar el anterior y actualizar el slot correspondiente
            borrarTurno(turnos2.get(paciente=paciente))

            # print('DEBUG: creando una entrada para el slot elegido')

            turnoSlotActual = TurnoSlot(fecha=fechaElegida, cupo=1, horaID=horaActual)
            turnoSlotActual.save()
            turno = Turno(paciente=user_info.paciente, turnoSlotID=turnoSlotActual,
                          centro=user_info.paciente.centro_vacunacion, horaturnoID=horaActual)
            turno.save()
            # print('DEBUG: ' + str(turno_data))
            turno_dic = {"turnoActual": turno}
            return render(request, 'turno_solicitado.html', turno_dic)
    else:
        # print('DEBUG: form is not valid')
        form = SolicitarTurnoForm()
        form2 = SolicitarTurnoForm2()

    # FALTA: enviar mail de turno
    return render(request, 'modificar_turno.html', {'form': form, 'form2': form2})

class PacienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return Paciente.objects.none()

        qs = Paciente.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

def registrarAplicacion_view(request):
    form = registrarAplicacionForm(request.POST)
    #if request.method == 'POST':
    if form.is_valid():
        aplicacion = form.save(commit=False)
        aplicacion.nombrevacuna = form.cleaned_data.get('nombrevacuna')
        aplicacion.fecha_de_aplicacion = form.cleaned_data.get('fehca_de_aplicacion')
        aplicacion.numero_de_lote = form.cleaned_data.get('numero_de_lote')
        aplicacion.id_paciente = form.cleaned_data.get('id_paciente')
        # aplicacion.id_vacunador = request.user.id
        aplicacion.id_vacunador = Vacunador.objects.get(pk=1)
        aplicacion.save()
        return render(request, 'aplicacion_ok.html')

    return render(request, 'registrar_aplicacion.html', {'form': form})


def obtenerCertificado_view(request):
    user = request.user.id
    if Aplicacion.objects.filter(id_paciente=user).exists():
        return generarPDF_view(request)
    else:
        return render(request, 'sin_vacunas_aplicadas.html')

def generarPDF_view(request):
    user = request.user.id
    paciente = Paciente.objects.get(user__id=user)
    userinfo = User.objects.get(id=user)
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    vacunas = Aplicacion.objects.filter(id_paciente=request.user.id).values_list('nombrevacuna')
    nombre = userinfo.paciente.first_name
    apellido = userinfo.paciente.last_name
    dni = userinfo.paciente.dni
    texto = pdf.beginText()
    texto.setTextOrigin(inch,10*inch)
    texto.setFont("Helvetica", 14)
    #pdf.drawImage(10,10, imagen)
    texto.textLine("Paciente: " + nombre + " " + apellido)
    texto.textLine("DNI: "+ dni)
    texto.textLine("Certifico que el paciente recibió las vacunas: ")
    vacs = []
    for vacuna in vacunas:
        vacs.append(vacuna[0])
    for line in vacs:
        texto.textLine(line)
    pdf.drawText(texto)
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="certificado.pdf")


def homeVacunador_view(request):
    return render(request, 'home_vac.html')

