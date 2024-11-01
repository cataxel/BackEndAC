from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response

from BackEndAC.publics.Generics.Respuesta import APIRespuesta
from usuarios.models import Roles, Usuario, Perfil
from usuarios.serializers import RolesSerializer, UsuarioSerializer, PerfilSerializer


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
        # Obtén el correo del request
        correo = request.data.get('correo')

        # Verifica si el correo tiene un formato válido
        if correo and not self.validar_correo(correo):
            return APIRespuesta(
                estado=False,
                mensaje='El correo debe ser válido.',
                data=None,
                codigoestado=status.HTTP_400_BAD_REQUEST
            ).to_response()

        # Procede con la creación del usuario si el correo es válido
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

    def validar_correo(self, correo):
        """
        Valida que el correo tenga el formato correcto.
        """
        import re
        # Expresión regular para validar un correo electrónico genérico
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, correo)

    def update(self, request, *args, **kwargs):
        """
        Maneja la actualización de un usuario existente.
        """
        instance = self.get_object()  # Obtiene el usuario a actualizar

        if isinstance(instance, Response):
            return instance  # Si instance es una respuesta, devuélvela directamente

        # Obtiene los datos de la solicitud
        nuevo_correo = request.data.get('correo', instance.correo)
        if nuevo_correo and not self.validar_correo(nuevo_correo):
            return APIRespuesta(
                estado=False,
                mensaje='El correo debe ser valido',
                data=None,
                codigoestado=status.HTTP_400_BAD_REQUEST
            ).to_response()

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            usuario = serializer.save()
            response = APIRespuesta(
                estado=True,
                mensaje='Usuario actualizado exitosamente.',
                data=serializer.data,
                codigoestado=status.HTTP_200_OK
            )
            return response.to_response()

        # Si hay errores de validación
        response = APIRespuesta(
            estado=False,
            mensaje='Error al actualizar el usuario.',
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

class PerfilViewSet(viewsets.ModelViewSet):
    serializer_class = PerfilSerializer
    queryset = Perfil.objects.all()

    def get_object(self):
        guid = self.kwargs.get('pk')
        try:
            # Búsqueda explícita por el campo 'guid'
            return Perfil.objects.get(guid=guid)
        except Perfil.DoesNotExist:
            response = APIRespuesta(
                estado=False,
                mensaje="El perfil no existe.",
                data=None,
                codigoestado=status.HTTP_404_NOT_FOUND
            )
            # Devuelve la respuesta en un formato apropiado
            return response.to_response()


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            perfil = serializer.save()
            headers = self.get_success_headers(serializer.data)

            response = APIRespuesta(
                estado=True,
                mensaje="Perfil creado exitosamente.",
                data=serializer.data,
                codigoestado=status.HTTP_201_CREATED
            )
            return response.to_response()
        response = APIRespuesta(
            estado=False,
            mensaje="Error al crear el perfil.",
            data=serializer.errors,
            codigoestado=status.HTTP_400_BAD_REQUEST
        )
        return response.to_response()

    def update(self, request, *args, **kwargs):
        try:
            # Obtener la instancia según el GUID de la URL
            instance = self.get_object()
        except Http404:
            response = APIRespuesta(
                estado=False,
                mensaje="Perfil no encontrado.",
                data=None,
                codigoestado=status.HTTP_404_NOT_FOUND
            )
            return response.to_response()

        # Procesar los datos del request usando el serializer
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            perfil = serializer.save()

            response = APIRespuesta(
                estado=True,
                mensaje="Perfil actualizado exitosamente.",
                data=serializer.data,
                codigoestado=status.HTTP_200_OK
            )
            return response.to_response()

        response = APIRespuesta(
            estado=False,
            mensaje="Error al actualizar el perfil.",
            data=serializer.errors,
            codigoestado=status.HTTP_400_BAD_REQUEST
        )
        return response.to_response()

    def destroy(self, request, *args, **kwargs):
        """
        Maneja la eliminación de un perfil por su GUID.
        """
        instance = self.get_object()  # Intenta obtener el objeto (usuario)

        if isinstance(instance, Response):
            return instance  # Si instance es una respuesta, devuélvela directamente

        # Elimina la instancia
        self.perform_destroy(instance)

        # Crear respuesta de éxito
        response = APIRespuesta(
            estado=True,
            mensaje="Datos del perfil eliminado exitosamente.",
            data=None,
            codigoestado=status.HTTP_204_NO_CONTENT
        )
        return response.to_response()


# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from usuarios.models import Usuario
from pymongo import MongoClient


class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        correo = request.data.get('correo')
        contraseña = request.data.get('contraseña')

        try:
            # Buscar al usuario por correo
            user = Usuario.objects.get(correo=correo)

            # Verificar la contraseña
            if check_password(contraseña, user.contraseña):
                refresh = RefreshToken.for_user(user)

                # Conectar a MongoDB
                client = MongoClient(
                    "mongodb+srv://beto:FEyR64Tyj1VFXo5I@sessions.byekg.mongodb.net/?retryWrites=true&w=majority&appName=Sessions")
                db = client["Sessions"]  # Nombre de la base de datos
                tokens_collection = db["tokens"]  # Nombre de la colección

                # Guardar el token en la colección
                token_data = {
                    'user_guid': str(user.guid),
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token)
                }
                tokens_collection.insert_one(token_data)

                # Cerrar conexión con MongoDB
                client.close()

                return Response({
                    'user_guid': str(user.guid),
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Contraseña incorrecta.'}, status=status.HTTP_401_UNAUTHORIZED)

        except Usuario.DoesNotExist:
            return Response({'detail': 'El usuario no existe.'}, status=status.HTTP_404_NOT_FOUND)
