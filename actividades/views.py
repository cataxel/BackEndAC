# Create your views here.
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import NotFound

from BackEndAC.publics.Generics.Respuesta import APIRespuesta
from usuarios.models import Usuario
from .models import Actividad, Grupo, Inscripcion
from .serializers import ActividadSerializer, GrupoSerializer, InscripcionSerializer



class ActividadViewSet(viewsets.ModelViewSet):
    serializer_class = ActividadSerializer
    queryset = Actividad.objects.all()
    lookup_field = 'guid'

    def retrieve(self, request, *args, **kwargs):
        try:
            actividad = self.get_object()
            serializer = self.get_serializer(actividad)
            return APIRespuesta(
                estado=True,
                mensaje='Actividad encontrada',
                data=serializer.data,
                codigoestado=status.HTTP_200_OK
            ).to_response()

        except NotFound:
            return APIRespuesta(
                estado=False,
                mensaje='Actividad no encontrada',
                codigoestado=status.HTTP_404_NOT_FOUND
            ).to_response()
        except Exception as e:
                return APIRespuesta(
                estado=False,
                mensaje=f'Error inesperado',
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return APIRespuesta(
                    estado=True,
                    mensaje='Actividad guardada',
                    data=serializer.data,
                    codigoestado=status.HTTP_200_OK
                ).to_response()
            else:
                return APIRespuesta(
                    estado=False,
                    mensaje='Error al guardar',
                    data=serializer.errors,
                    codigoestado=status.HTTP_400_BAD_REQUEST
                ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje=f'Error inesperado',
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

    def update(self, request, *args, **kwargs):
        try:
            # Obtener la actividad a actualizar
            actividad = self.get_object()

            # Crear el serializer con la instancia de actividad y los datos del request
            serializer = self.get_serializer(actividad, data=request.data)

            # Validar y guardar los cambios
            if serializer.is_valid():
                serializer.save()
                return APIRespuesta(
                    estado=True,
                    mensaje='Actividad actualizada',
                    data=serializer.data,
                    codigoestado=status.HTTP_200_OK
                ).to_response()
            else:
                return APIRespuesta(
                    estado=False,
                    mensaje='Error al actualizar',
                    data=serializer.errors,
                    codigoestado=status.HTTP_400_BAD_REQUEST
                ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje=f'Error inesperado',
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

    def destroy(self, request, *args, **kwargs):
        try:
            # Obtener la actividad a eliminar
            actividad = self.get_object()

            # Eliminar la actividad
            actividad.delete()

            return APIRespuesta(
                estado=True,
                mensaje='Actividad eliminada exitosamente',
                data=None,
                codigoestado=status.HTTP_204_NO_CONTENT
            ).to_response()

        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje=f'Error al eliminar la actividad',
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()





class GrupoViewSet(viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all()
    lookup_field = 'guid'

    def retrieve(self, request, *args, **kwargs):
        try:
            grupo = self.get_object()
            serializer = self.get_serializer(grupo)
            return APIRespuesta(
                estado=True,
                mensaje='Grupo encontrado',
                data=serializer.data,
                codigoestado=status.HTTP_200_OK
            ).to_response()

        except NotFound:
            return APIRespuesta(
                estado=False,
                mensaje='Grupo no encontrado',
                codigoestado=status.HTTP_404_NOT_FOUND
            ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje=f'Error inesperado',
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return APIRespuesta(
                    estado=True,
                    mensaje='Grupo creado exitosamente',
                    data=serializer.data,
                    codigoestado=status.HTTP_201_CREATED
                ).to_response()
            else:
                return APIRespuesta(
                    estado=False,
                    mensaje='Error al crear el grupo',
                    data=serializer.errors,
                    codigoestado=status.HTTP_400_BAD_REQUEST
                ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje=f'Error inesperado',
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

    def update(self, request, *args, **kwargs):
        try:
            grupo = self.get_object()
            serializer = self.get_serializer(grupo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return APIRespuesta(
                    estado=True,
                    mensaje='Grupo actualizado exitosamente',
                    data=serializer.data,
                    codigoestado=status.HTTP_200_OK
                ).to_response()
            else:
                return APIRespuesta(
                    estado=False,
                    mensaje='Error al actualizar el grupo',
                    data=serializer.errors,
                    codigoestado=status.HTTP_400_BAD_REQUEST
                ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje=f'Error inesperado',
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

    def destroy(self, request, *args, **kwargs):
        try:
            grupo = self.get_object()
            grupo.delete()
            return APIRespuesta(
                estado=True,
                mensaje='Grupo eliminado exitosamente',
                data=None,
                codigoestado=status.HTTP_204_NO_CONTENT
            ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje='Error al eliminar el grupo',
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()



class InscripcionViewSet(viewsets.ModelViewSet):
    serializer_class = InscripcionSerializer
    queryset = Inscripcion.objects.all()
    lookup_field = 'guid'

    def retrieve(self, request, *args, **kwargs):
        try:
            inscripcion = self.get_object()
            serializer = self.get_serializer(inscripcion)
            return APIRespuesta(
                estado=True,
                mensaje='Inscripcion encontrada',
                data=serializer.data,
                codigoestado=status.HTTP_200_OK
            ).to_response()

        except NotFound:
            return APIRespuesta(
                estado=False,
                mensaje='Inscripcion no encontrada',
                codigoestado=status.HTTP_404_NOT_FOUND
            ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje=f'Error inesperado',
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

    def create(self, request, *args, **kwargs):
        try:
            # Obtener los datos del request
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Extraer los datos necesarios para validar duplicados
                usuario = serializer.validated_data.get('usuario')
                grupo = serializer.validated_data.get('grupo')

                # Verificar si ya existe una inscripción con los mismos datos
                if Inscripcion.objects.filter(usuario=usuario, grupo=grupo).exists():
                    return APIRespuesta(
                        estado=False,
                        mensaje='Ya existe una inscripción para este usuario en este evento',
                        data={},
                        codigoestado=status.HTTP_400_BAD_REQUEST
                    ).to_response()

                # Si no hay duplicados, guardar la inscripción
                serializer.save()
                return APIRespuesta(
                    estado=True,
                    mensaje='Inscripción guardada',
                    data=serializer.data,
                    codigoestado=status.HTTP_200_OK
                ).to_response()
            else:
                return APIRespuesta(
                    estado=False,
                    mensaje='Error al guardar',
                    data=serializer.errors,
                    codigoestado=status.HTTP_400_BAD_REQUEST
                ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje=f'Error inesperado',
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

    def update(self, request, *args, **kwargs):
        try:
            # Obtener la inscripción a actualizar
            inscripcion = self.get_object()

            # Crear el serializer con la instancia actual y los datos del request
            serializer = self.get_serializer(inscripcion, data=request.data)

            # Validar los datos
            if serializer.is_valid():
                # Extraer los datos necesarios para validar duplicados
                usuario = serializer.validated_data.get('usuario')
                grupo = serializer.validated_data.get('grupo')

                # Verificar si ya existe otra inscripción con los mismos datos
                if Inscripcion.objects.filter(
                        usuario=usuario,
                        grupo=grupo
                ).exclude(id=inscripcion.id).exists():
                    return APIRespuesta(
                        estado=False,
                        mensaje='Ya existe otra inscripción para este usuario en este evento',
                        data={},
                        codigoestado=status.HTTP_400_BAD_REQUEST
                    ).to_response()

                # Si no hay duplicados, guardar los cambios
                serializer.save()
                return APIRespuesta(
                    estado=True,
                    mensaje='Inscripción actualizada',
                    data=serializer.data,
                    codigoestado=status.HTTP_200_OK
                ).to_response()
            else:
                return APIRespuesta(
                    estado=False,
                    mensaje='Error al actualizar',
                    data=serializer.errors,
                    codigoestado=status.HTTP_400_BAD_REQUEST
                ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje='Error inesperado',
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

    def destroy(self, request, *args, **kwargs):
        try:
            # Obtener la inscripcion a eliminar
            inscripcion = self.get_object()

            # Eliminar la inscripcion
            inscripcion.delete()

            return APIRespuesta(
                estado=True,
                mensaje='Inscripcion eliminada exitosamente',
                data=None,
                codigoestado=status.HTTP_204_NO_CONTENT
            ).to_response()

        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje=f'Error al eliminar la inscripcion',
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()