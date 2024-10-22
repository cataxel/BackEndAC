from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from BackEndAC.publics.Generics.Respuesta import APIRespuesta
from usuarios.models import Roles, Usuario
from usuarios.serializers import RolesSerializer, UsuarioSerializer


class RolViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
    #permission_classes = [permissions.IsAuthenticated]


class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

    def get_object(self):
        """
        Sobrescribe este metodo para buscar el usuario por su GUID.
        """
        guid = self.kwargs.get('pk')  # `pk` contendrá el GUID de la URL
        try:
            return Usuario.objects.get(guid=guid)  # Busca el usuario por su GUID
        except Usuario.DoesNotExist:
            # En lugar de lanzar una excepción, devolvemos una respuesta APIRespuesta
            response = APIRespuesta(
                estado=False,
                mensaje="El usuario no existe.",
                data=None,
                codigoestado=status.HTTP_404_NOT_FOUND
            )
            # Devuelve la respuesta en un formato apropiado
            return response.to_response()

    def create(self, request, *args, **kwargs):
        """
        Maneja la creación de un nuevo usuario.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            usuario = serializer.save()
            headers = self.get_success_headers(serializer.data)

            # Crear respuesta de éxito
            response = APIRespuesta(
                estado=True,
                mensaje="Usuario creado exitosamente.",
                data=serializer.data,
                codigoestado=status.HTTP_201_CREATED
            )
            return response.to_response()

        # Si hay errores de validación
        response = APIRespuesta(
            estado=False,
            mensaje="Error al crear el usuario.",
            data=serializer.errors,
            codigoestado=status.HTTP_400_BAD_REQUEST
        )
        return response.to_response()

    def destroy(self, request, *args, **kwargs):
        """
        Maneja la eliminación de un usuario por su GUID.
        """
        instance = self.get_object()  # Intenta obtener el objeto (usuario)

        if isinstance(instance, Response):
            return instance  # Si instance es una respuesta, devuélvela directamente

        # Elimina la instancia
        self.perform_destroy(instance)

        # Crear respuesta de éxito
        response = APIRespuesta(
            estado=True,
            mensaje="Usuario eliminado exitosamente.",
            data=None,
            codigoestado=status.HTTP_204_NO_CONTENT
        )
        return response.to_response()
