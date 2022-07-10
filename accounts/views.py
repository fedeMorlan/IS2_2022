from asyncio.windows_events import NULL
from lib2to3.pgen2.pgen import PgenGrammar
from logging import root
from struct import pack
from django.forms import ImageField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import date
# Create your views here.

# builtin: UserCreationForm para registro
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import CentroDeVacunacion, Paciente, VacunasAnteriores, Aplicacion, TurnoSlot, Turno, HoraTurno
from .forms import *
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from PIL import Image, ImageChops
import glob, io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import os
from accounts.models import Vacunador
from django.conf.urls.static import static
from datetime import datetime

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
        # user2 = form2.save(commit=False)
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
    # else:
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
    vacunas = Aplicacion.objects.filter(id_paciente=request.user.id).values_list('nombrevacuna', 'fecha_de_aplicacion',
                                                                                 'numero_de_lote')
    if not vacunas:
        # lo pongo como parte de una tupla porque el html muestra la request.data por campos, si mando el string me muestra renglones de una letra
        request.data = ("Usted no tiene vacunas aplicadas.",)
    else:
        request.data = vacunas
    return render(request, 'vacunas_aplicadas.html')


def custom_login(request, user):
    # get previous seesion_key for signal
    prev_session_key = request.session.session_key

    """ 
        original code

    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
    login(request, user)
    # send extra argument prev_session_key
    user_logged_in.send(sender=user.__class__, request=request, user=user, prev_session_key=prev_session_key)
    return user


class CustomLoginView(LoginView):
    def form_valid(self, form):
        """Security check complete. Log the user in."""

        # changed default login
        user = custom_login(self.request, form.get_user())
        if user:
            if user.paciente.dueño:

                return HttpResponseRedirect('../home_administrador')
                #return redirect('home dueño', user)
            elif user.paciente.vacunador:
                return redirect('home vacunador')
            else:
                print('paciente')
                return redirect('home')

def registrarVacunador_view(request):
    form = SignUpForm(request.POST, request.FILES)
    form2 = SignUpForm2(request.POST, request.FILES)
    if form.is_valid() and form2.is_valid():
        user = form.save()
        # user2 = form2.save(commit=False)
        user.paciente.refresh_from_db()
        user.paciente.dni = form.cleaned_data.get('dni')
        user.paciente.first_name = form.cleaned_data.get('first_name')
        user.paciente.last_name = form.cleaned_data.get('last_name')
        user.paciente.email = form.cleaned_data.get('email')
        user.paciente.nacimiento = form2.cleaned_data['nacimiento']
        user.paciente.comorbilidad = form2.cleaned_data.get('comorbilidad')
        user.paciente.vacunador = True
        vacunador = Vacunador(email=user.paciente.email, dni=user.paciente.dni, user=user)
        user.save()
        vacunador.save()
        user.paciente.save()
        #username = form.cleaned_data.get('username')
        #password = form.cleaned_data.get('password1')
        #user = authenticate(username=username, password=password)
        #login(request, user)
        return redirect('registrar vacunador exito')
    # descomentar esto es poco informativo para el user
    # else:
    #    form = SignUpForm(instance=User)
    #    form2 = SignUpForm2(instance=Paciente)
    return render(request, 'registrar_vacunador.html', {'form': form, 'form2': form2})

def registrarVacunadorExito_view(request):
    return render(request, 'registrar_vacunador_exito.html')

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
                if (request.FILES['frente'].name == request.FILES['dorso'].name):
                    messages.error(request, "Cargue dos imagenes distinstas.")
                else:
                    frente = form.cleaned_data.get('frente')
                    dorso = form.cleaned_data.get('dorso')

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
        turno_dic = {"turnoActual": turno_data, "previo": "ok"}
        return render(request, 'turno_solicitado.html', turno_dic)

    # ----------- PEDIR TURNO --------------------
    # elegir fecha y hora de turno
    form = SolicitarTurnoForm(request.POST, request.FILES)
    form2 = SolicitarTurnoForm2(request.POST, request.FILES, user=request.user)

    if request.method == 'POST' and form.is_valid() and form2.is_valid():
        fechaElegida = form.cleaned_data['fecha']
        horaElegida = form2.cleaned_data.get('horaturnoID').hora
        horaActual = horas.filter(hora=horaElegida).get()
        vacunas = form2.cleaned_data.get('nombrevacuna')
        vacuna = vacunas[0]
        if len(vacunas) > 1:
            vacuna2 = vacunas[1]
        else:
            vacuna2 = None


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

        # si la fecha existe en ese centro
        if turnos2.filter(centro=paciente.centro_vacunacion, horaturnoID=horaActual).exists() and \
                turnos.filter(fecha=fechaElegida, horaID=horaActual).exists() and ok:
            turnoActual=turnos2.get(centro=paciente.centro_vacunacion, horaturnoID=horaActual)
            turnoSlotActual = turnos.get(fecha=fechaElegida, horaID=horaActual, slotID=turnoActual.turnoSlotID.slotID)
            # si hay cupo disponible
            if turnoSlotActual.cupo < 5:
                # incrementar el contador y guardar turno
                turnoSlotActual.cupo += 1
                turnoSlotActual.save()
                turno = Turno(paciente=user_info.paciente, turnoSlotID=turnoSlotActual,
                              centro=user_info.paciente.centro_vacunacion, horaturnoID=horaActual,
                              vacunaID=vacuna, vacuna2ID=vacuna2)
                turno.save()
                turno_data = turnos2.get(paciente=paciente)
                turno_dic = {"turnoActual": turno_data}
                return render(request, 'turno_solicitado.html', turno_dic)
            # si no hay cupo
            else:
                # mensaje que indica que no hay cupo
                messages.error(request, "No hay mas turnos disponibles en este horario")

        # si la fecha no existe
        elif ok:
            turnoSlotActual = TurnoSlot(fecha=fechaElegida, cupo=1, horaID=horaActual)
            turnoSlotActual.save()
            turno = Turno(paciente=user_info.paciente, turnoSlotID=turnoSlotActual,
                          centro=user_info.paciente.centro_vacunacion, horaturnoID=horaActual,
                          vacunaID=vacuna, vacuna2ID=vacuna2)
            turno.save()
            # crear fecha y guardar turno
            turno_data = turnos2.get(paciente=paciente)
            turno_dic = {"turnoActual": turno_data}
            return render(request, 'turno_solicitado.html', turno_dic)
    else:
        form = SolicitarTurnoForm()
        form2 = SolicitarTurnoForm2(user=request.user)

    # FALTA: enviar mail de turno
    return render(request, 'solicitar_turno.html', {'form': form, 'form2': form2})


def borrarTurno(turno):
    # aumentar la capacidad del turnoslot correspondiente
    tSlotActual = TurnoSlot.objects.get(slotID=turno.turnoSlotID.slotID)
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
    form2 = SolicitarTurnoForm2(request.POST, request.FILES, user=request.user)
    turnos = TurnoSlot.objects
    turnos2 = Turno.objects
    horas = HoraTurno.objects
    if request.method == 'POST' and form.is_valid() and form2.is_valid():
        fechaElegida = form.cleaned_data['fecha']
        horaElegida = form2.cleaned_data.get('horaturnoID').hora
        horaActual = horas.filter(hora=horaElegida).get()
        vacunas = form2.cleaned_data.get('nombrevacuna')
        vacuna = vacunas[0]
        if len(vacunas) > 1:
            vacuna2 = vacunas[1]
        else:
            vacuna2 = None

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

        # si la fecha existe
        if turnos2.filter(centro=paciente.centro_vacunacion, horaturnoID=horaActual).exists() and \
                turnos.filter(fecha=fechaElegida, horaID=horaActual).exists() and ok:
            turnoActual = turnos2.get(centro=paciente.centro_vacunacion, horaturnoID=horaActual)
            turnoSlotActual = turnos.get(fecha=fechaElegida, horaID=horaActual, slotID=turnoActual.turnoSlotID.slotID)
            # si hay cupo disponible
            if turnoSlotActual.cupo < 5:

                # eliminar el anterior y actualizar el slot correspondiente
                borrarTurno(turnos2.get(paciente=paciente))

                # incrementar el contador y guardar turno
                turnoSlotActual.refresh_from_db()
                turnoSlotActual.cupo += 1
                turnoSlotActual.save()
                turno = Turno(paciente=user_info.paciente, turnoSlotID=turnoSlotActual,
                              centro=user_info.paciente.centro_vacunacion, horaturnoID=horaActual,
                              vacunaID=vacuna, vacuna2ID=vacuna2)
                turno.save()

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

            turnoSlotActual = TurnoSlot(fecha=fechaElegida, cupo=1, horaID=horaActual)
            turnoSlotActual.save()
            turno = Turno(paciente=user_info.paciente, turnoSlotID=turnoSlotActual,
                          centro=user_info.paciente.centro_vacunacion, horaturnoID=horaActual,
                          vacunaID=vacuna, vacuna2ID=vacuna2)
            turno.save()
            turno_dic = {"turnoActual": turno}
            return render(request, 'turno_solicitado.html', turno_dic)
    else:
        form = SolicitarTurnoForm()
        form2 = SolicitarTurnoForm2(user=request.user)

    # FALTA: enviar mail de turno
    return render(request, 'modificar_turno.html', {'form': form, 'form2': form2})


# class PacienteAutocomplete(autocomplete.Select2QuerySetView):
#    def get_queryset(self):
#
#        if not self.request.user.is_authenticated:
#            return Paciente.objects.none()
#
#        qs = Paciente.objects.all()
#
#        if self.q:
#            qs = qs.filter(name__istartswith=self.q)
#
#        return qs

def registrarAplicacion_view(request):
    form = registrarAplicacionForm(request.POST)
    # if request.method == 'POST':
    if form.is_valid():
        aplicacion = form.save(commit=False)
        aplicacion.nombrevacuna = form.cleaned_data.get('nombrevacuna')
        aplicacion.fecha_de_aplicacion = form.cleaned_data.get('fecha_de_aplicacion')
        aplicacion.numero_de_lote = form.cleaned_data.get('numero_de_lote')
        aplicacion.id_paciente = form.cleaned_data.get('id_paciente')
        aplicacion.id_vacunador = Vacunador.objects.get(pk=request.user.id)
        # aplicacion.id_vacunador = Vacunador.objects.get(pk=9)
        aplicacion.save()

        # registrar en tabla VacunasAnteriores la aplicacion actual
        vacuna = VacunasAnteriores.objects.get(user=aplicacion.id_paciente.user)
        if str(aplicacion.nombrevacuna) == 'COVID 1':
            vacuna.covid_1 = True
        elif str(aplicacion.nombrevacuna) == 'COVID 2':
            vacuna.covid_2 = True
        elif str(aplicacion.nombrevacuna) == 'gripe':
            vacuna.gripe = True
        elif str(aplicacion.nombrevacuna) == 'fiebre amarilla':
            vacuna.fiebre_amarilla = True
        vacuna.save()
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
    texto.setTextOrigin(inch, 10 * inch)
    texto.setFont("Helvetica", 14)

    pdf.drawImage('static/img/Logo_VacunAssist_1.png', 450, 700, width=120, height=120)
    pdf.drawImage('static/img/qr.png', 200, 180, width=190, height=190)

    texto.textLine("El paciente: ")
    texto.textLine(nombre + " " + apellido)
    texto.textLine("DNI: " + dni)
    texto.textLine("Recibio las siguientes dosis: ")
    vacs = []
    for vacuna in vacunas:
        vacs.append(str(vacuna[0]))
    for line in vacs:
        texto.textLine(line)
    pdf.drawString(175, 160, "Para mas información, lea el código QR con la cámara su teléfono")
    pdf.drawText(texto)
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="certificado.pdf")


def homeVacunador_view(request):

    return render(request, 'home_vac.html')


def homeAdministrador_view(request):

    return render(request, 'home_administrador.html')


def emailInvalido_view(request):
    return render(request, 'email_invalido.html')


def verTurnosDelDia_view(request):
    hoy = datetime.today().strftime('%Y-%m-%d')
    turnos_del_dia = Turno.objects.filter(turnoSlotID__fecha=hoy)
    turnoDic = {'turnos': turnos_del_dia, 'hoy': hoy}
    return render(request, 'turnos_del_dia_todos.html', turnoDic)


def verTurnosDelDiaCentro_view(request):
    hoy = datetime.today().strftime('%Y-%m-%d')
    turnos_del_dia = Turno.objects.filter(turnoSlotID__fecha=hoy)
    form = TurnosDelDiaPorCentroForm(request.POST)
    centro = ''
    if form.is_valid():
        form.save(commit=False)
        centro = form.cleaned_data.get('centro')
        turnos_del_dia = Turno.objects.filter(centro__nombre=centro).filter(turnoSlotID__fecha=hoy)
    if not turnos_del_dia or centro == '':
        turnos_del_dia = ('No hay turnos para mostrar',)
    turnoDic = {'turnos': turnos_del_dia, 'hoy': hoy, 'centro': centro, 'form': form}
    return render(request, 'turnos_del_dia_centro.html', turnoDic)
