# accounts/urls.py
from django.urls import path

# from .views import SignUpView
from .views import *
from .views import userinfo_view, modificarDatos_view, validarIdentidadRenaper_view

urlpatterns = [
    # path("signup/", SignUpView.as_view(), name="signup"),
    path('signup/', signup_view, name="signup"),
    path('informacion/', userinfo_view, name="userinfo"),
    path('vacunasant/', vacunasAnteriores_view, name='Vacunas anteriores'),
    path('cambiarcontrasena/', cambiarContraseña_view, name='Cambiar contraseña'),
    path('elegir_centro/', elegirCentro_view, name='Elegir centro de vacunacion'),
    path('modificar_datos/', modificarDatos_view, name='Modificar datos personales'),
    path('validar_identidad/', validarIdentidadRenaper_view, name='Validar identidad con RENAPER'),

]
