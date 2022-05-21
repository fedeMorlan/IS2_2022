# accounts/urls.py
from django.urls import path

# from .views import SignUpView
<<<<<<< HEAD
from .views import signup_view, vacunasAnteriores_view, userinfo_view, elegirCentro_view, cambiarContraseña_view

=======
from .views import *
from .views import userinfo_view
>>>>>>> 856d9a216734950c926e57902d9746624bca4538

urlpatterns = [
    # path("signup/", SignUpView.as_view(), name="signup"),
    path('signup/', signup_view, name="signup"),
    path('informacion/', userinfo_view, name="userinfo"),
    path('vacunasant/', vacunasAnteriores_view, name='Vacunas anteriores'),
    path('cambiarcontrasena/', cambiarContraseña_view, name='Cambiar contraseña'),
    path('elegir_centro/', elegirCentro_view, name='Elegir centro de vacunacion')
<<<<<<< HEAD
]
=======
    ]
>>>>>>> 856d9a216734950c926e57902d9746624bca4538
