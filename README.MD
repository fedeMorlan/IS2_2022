Funcionalidad ya implementada:
registrarse, iniciar sesion, cerrar sesion, recuperar contrasena

como:

1)
crear una maquina virtual local dentro de la misma carpeta copiando en consola lo siguiente:

# Windows
> python -m venv .venv
> .venv\Scripts\activate
(.venv) > python -m pip install django~=4.0.0

esta carpeta que nos crea automaticamente queda excluida para el push gracias al archivo ".gitignore" que contiene la .venv para excluirla (por seguridad)

1) Si ya tenemos la maquina virtual, ingresar en esa maquina virtual usando:
> .venv\Scripts\activate
> (.venv) >

2) iniciar el server local con 
(.venv) > python manage.py runserver

3) ingresar a un navegador y entrar a 127.0.0.1:8000
   si no anda, ingresar en otro navegador o en modo incognito

Para cargar la base de datos:
   python manage.py loaddata centroVacunacion.json
   python manage.py loaddata horasTurno.json
   python manage.py loaddata vacunas.json