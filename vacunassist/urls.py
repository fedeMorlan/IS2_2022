"""vacunassist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path  # new
from django.views.generic.base import TemplateView
from accounts.views import CustomLoginView
from accounts.forms import CustomEmailValidationOnForgotPassword

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("pages.urls")),   # new

    # esto es para el registro de users
    # https://learndjango.com/tutorials/django-signup-tutorial
    path("accounts/", include("accounts.urls")),  # new
    # esto es para el logueo de users generados a traves del superuser de django
    # https://learndjango.com/tutorials/django-login-and-logout-tutorial
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path("accounts/", include("django.contrib.auth.urls")),  # new
    #re_path(r'^password-reset/$',
    #'django.contrib.auth.views.password_reset',
    #{'post_reset_redirect': '/user/password/reset/done/',
    # 'html_email_template_name': 'registration/password_reset_email.html',
    # 'password_reset_form': CustomEmailValidationOnForgotPassword},
    #name="password_reset"),
]
