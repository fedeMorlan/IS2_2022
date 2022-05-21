# accounts/urls.py
from django.urls import path

# from .views import SignUpView
from .views import signup_view, vacunasAnteriores_view, userinfo_view, elegirCentro_view, cambiarContraseña_view


urlpatterns = [
    # path("signup/", SignUpView.as_view(), name="signup"),
    path('signup/', signup_view, name="signup"),
    path('informacion/', userinfo_view, name="userinfo"),
    path('vacunasant/', vacunasAnteriores_view, name='Vacunas anteriores'),
    path('cambiarcontrasena/', cambiarContraseña_view, name='Cambiar contraseña'),
    path('elegir_centro/', elegirCentro_view, name='Elegir centro de vacunacion')
]