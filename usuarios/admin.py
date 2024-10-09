from django.contrib import admin
from .models import Roles, Usuario

# Registrar el modelo Roles en el administrador de Django
admin.site.register(Roles)

# Registrar el modelo Usuario en el administrador de Django
admin.site.register(Usuario)
