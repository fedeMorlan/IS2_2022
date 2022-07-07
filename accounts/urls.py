# accounts/urls.py
from django.urls import path, re_path
from django.contrib.auth.views import PasswordResetView
# from .views import SignUpView
from .views import *
from accounts.forms import EmailValidationOnForgotPassword

urlpatterns = [
    # path("signup/", SignUpView.as_view(), name="signup"),
    path('signup/', signup_view, name="signup"),
    path('informacion/', userinfo_view, name="userinfo"),
    path('vacunasant/', vacunasAnteriores_view, name='Vacunas anteriores'),
    path('cambiarcontrasena/', cambiarContraseña_view, name='Cambiar contraseña'),
    path('elegir_centro/', elegirCentro_view, name='Elegir centro de vacunacion'),
    path('modificar_datos/', modificarDatos_view, name='Modificar datos personales'),
    path('validar_identidad/', validarIdentidadRenaper_view, name='Validar identidad con RENAPER'),
    path('solicitar_turno/', solicitarTurno_view, name='Solicitar turno'),
    path('ver_vacunas_aplicadas/', verVacunasAplicadas_view, name='Ver mis vacunas aplicadas'),
    path('registrar_aplicacion/', registrarAplicacion_view, name='Registrar aplicacion de vacuna'),
    #path('paciente-autocomplete/', PacienteAutocomplete.as_view(), name='paciente-autocomplete'),
    path('turno_pendiente/', turnoPendiente_view, name='turno pendiente'),
    path('cancelar_turno/', cancelarTurno_view, name='cancelar turno'),
    path('modificar_turno/', modificarTurno_view, name='modificar turno'),
    path('certificado/', obtenerCertificado_view, name='obtener certificado'),
    path('home_vacunador/', homeVacunador_view, name='home vacunador'),
    path('email_invalido/', emailInvalido_view, name='email invalido'),
    path('turnos_del_dia_todos/', verTurnosDelDia_view, name='todos los turnos del dia'),
    path('turnos_del_dia_centro/', verTurnosDelDiaCentro_view, name='turnos del dia por centro'),
    path('password_reset/', PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword), name='password_reset'),
    path('home_administrador/', homeAdministrador_view, name='home dueño'),
    path('registrar_vacunador/', registrarVacunador_view, name='registrar vacunador'),
    path('registrar_vacunador/exito', registrarVacunadorExito_view, name='registrar vacunador exito'),
    ]

