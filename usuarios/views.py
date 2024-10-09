from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.response import Response

from usuarios.models import Roles, Usuario
from usuarios.serializers import RolesSerializer, UsuarioSerializer


class RolViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo usuario.

        Args:
            request (Request): La petición HTTP.
            *args: Argumentos adicionales.
            **kwargs: Argumentos con nombre adicionales.

        Returns:
            Response: La respuesta HTTP.
        """
        data = request.data.copy()
        if 'contraseña' in data:
            data['contraseña'] = make_password(data['contraseña'])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)