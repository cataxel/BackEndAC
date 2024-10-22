from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from usuarios.models import Roles, Usuario
from usuarios.serializers import RolesSerializer, UsuarioSerializer


class RolViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
    #permission_classes = [permissions.IsAuthenticated]


class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()
    #permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Maneja la creación de un nuevo usuario.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        """
        Maneja la eliminación de un usuario.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        """
        Elimina una instancia de usuario.
        """
        instance.delete()
