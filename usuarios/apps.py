from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'


    def ready(self):
        from .models import create_roles
        post_migrate.connect(create_roles, sender=self)
