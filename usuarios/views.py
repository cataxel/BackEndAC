from django.contrib.auth.hashers import check_password
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from BackEndAC.publics.Generics.Respuesta import APIRespuesta
from BackEndAC.publics.Utils.Auto import RolePermission
from BackEndAC.publics.Utils.mongodb_client import MongoDBClient
from integracion.views import CloudinaryImageView
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
            # Devuelve una respuesta en lugar de pasar al serializador
            response = APIRespuesta(
                estado=False,
                mensaje="El usuario no existe.",
                data=None,
                codigoestado=status.HTTP_404_NOT_FOUND
            )
            return response.to_response()

    def retrieve(self, request,*args, **kwargs):
        usuario = self.get_object()
        if type(usuario) == Usuario:
            serializer = UsuarioSerializer(usuario)
            return APIRespuesta(
                estado= True,
                mensaje="Usuario obtenido exitosamente",
                data=serializer.data,
                codigoestado=status.HTTP_200_OK
            ).to_response()
        return usuario


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
        user = self.get_object()
        user.delete()

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

    def retrieve(self, request, *args, **kwargs):
        """
        Sobrescribe el metodo retrieve para buscar un perfil por el GUID del usuario.
        """
        usuario_guid = kwargs.get('pk')  # Obtén el GUID del usuario desde la URL
        try:
            perfil = Perfil.objects.get(usuario_guid=usuario_guid)  # Busca el perfil por usuario__guid
            serializer = self.get_serializer(perfil)
            return APIRespuesta(
                estado=True,
                mensaje="Perfil encontrado exitosamente.",
                data=serializer.data,
                codigoestado=status.HTTP_200_OK
            ).to_response()
        except Perfil.DoesNotExist:
            return APIRespuesta(
                estado=False,
                mensaje="No se encontró un perfil para el usuario especificado.",
                data=None,
                codigoestado=status.HTTP_404_NOT_FOUND
            ).to_response()

    def create(self, request, *args, **kwargs):
        data = request.data  # Los datos enviados en la solicitud

        # Procesar los datos del perfil
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            perfil = serializer.save()

            return APIRespuesta(
                estado=True,
                mensaje="Perfil creado exitosamente.",
                data=serializer.data,
                codigoestado=status.HTTP_201_CREATED
            ).to_response()

        return APIRespuesta(
            estado=False,
            mensaje="Error al crear el perfil.",
            data=serializer.errors,
            codigoestado=status.HTTP_400_BAD_REQUEST
        ).to_response()

    def update(self, request, *args, **kwargs):
        try:
            # Obtener la instancia según el GUID de la URL
            instance = self.get_object()
        except Http404:
            return APIRespuesta(
                estado=False,
                mensaje="Perfil no encontrado.",
                data=None,
                codigoestado=status.HTTP_404_NOT_FOUND
            ).to_response()

        # Si existe un archivo, procesarlo antes de guardar
        file = request.FILES.get('file')  # Usar 'file' para mantener consistencia con create
        if file:
            try:
                # Subir imagen a Cloudinary usando la vista predefinida
                upload_view = CloudinaryImageView()
                upload_request = {
                    "FILES": {"file": file},  # Simular la estructura de request para la vista
                }
                cloudinary_response = upload_view.post(upload_request)

                if cloudinary_response.data['estado']:
                    # Actualizar la URL de la imagen en el modelo
                    instance.imagen_url = cloudinary_response.data['data']['secure_url']
                else:
                    return APIRespuesta(
                        estado=False,
                        mensaje="Error al subir la imagen.",
                        data=cloudinary_response.data['mensaje'],
                        codigoestado=status.HTTP_400_BAD_REQUEST
                    ).to_response()
            except Exception as e:
                return APIRespuesta(
                    estado=False,
                    mensaje="Error al procesar la imagen.",
                    data=str(e),
                    codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
                ).to_response()

        # Procesar los datos del request usando el serializer
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            perfil = serializer.save()

            return APIRespuesta(
                estado=True,
                mensaje="Perfil actualizado exitosamente.",
                data=serializer.data,
                codigoestado=status.HTTP_200_OK
            ).to_response()

        return APIRespuesta(
            estado=False,
            mensaje="Error al actualizar el perfil.",
            data=serializer.errors,
            codigoestado=status.HTTP_400_BAD_REQUEST
        ).to_response()

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


class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        correo = request.data.get('correo')
        contraseña = request.data.get('contraseña')

        try:
            # Buscar al usuario por correo
            user = Usuario.objects.get(correo=correo)

            # Verificar la contraseña
            if check_password(contraseña, user.contraseña):
                # Generar los tokens manualmente
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                # Agregar el rol al token (puedes agregar más campos si lo necesitas)
                access_token['rol'] = str(user.rol.guid)

                # Guardar el token en MongoDB
                mongo_client = MongoDBClient(db_name="Sessions")
                mongo_client.connect()
                tokens_collection = mongo_client.get_collection("tokens")

                token_data = {
                    'user_guid': str(user.guid),
                    'refresh_token': str(refresh),
                    'access_token': str(access_token)
                }
                tokens_collection.insert_one(token_data)
                mongo_client.close()

                # Responder con los tokens
                response = APIRespuesta(
                    estado=True,
                    mensaje="Inicio de sesión exitoso.",
                    data={
                        'user_guid': str(user.guid),
                        'refresh': str(refresh),
                        'access': str(access_token)
                    },
                    codigoestado=status.HTTP_200_OK
                )
                return response.to_response()

            else:
                # Contraseña incorrecta
                response = APIRespuesta(
                    estado=False,
                    mensaje="Contraseña incorrecta.",
                    codigoestado=status.HTTP_401_UNAUTHORIZED
                )
                return response.to_response()

        except Usuario.DoesNotExist:
            # Usuario no existe
            response = APIRespuesta(
                estado=False,
                mensaje="El usuario no existe.",
                codigoestado=status.HTTP_404_NOT_FOUND
            )
            return response.to_response()


class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        # Obtener el token JWT de los encabezados
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise PermissionDenied("No se proporcionó un token de autenticación.")

        # El token generalmente se pasa en el formato "Bearer <token>"
        token = auth_header.split(" ")[1]

        # Usar JWTAuthentication para verificar y decodificar el token
        jwt_authenticator = JWTAuthentication()
        try:
            # Verificar y decodificar el token para obtener al usuario
            user, _ = jwt_authenticator.authenticate(request)
        except Exception as e:
            raise PermissionDenied(f"Autenticación fallida: {str(e)}")

        # Aquí puedes hacer lo que desees con el token, como revocar o eliminar el token guardado
        # En este caso, eliminamos el token de MongoDB (si lo estás almacenando)
        mongo_client = MongoDBClient(db_name="Sessions")
        mongo_client.connect()

        print(user)
        tokens_collection = mongo_client.get_collection("tokens")

        # Verifica si el user_guid está disponible
        if not user or not hasattr(user, 'guid'):
            raise PermissionDenied("No se pudo encontrar el usuario para hacer logout.")

        # Eliminar el token de MongoDB por el user_guid
        tokens_collection.delete_many({'user_guid': str(user.guid)})
        mongo_client.close()

        # Responder con un mensaje de éxito
        return Response({
            "estado": True,
            "mensaje": "Logout exitoso. El token ha sido revocado.",
        }, status=200)