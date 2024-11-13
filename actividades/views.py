

# Create your views here.
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import NotFound

from BackEndAC.publics.Generics.Respuesta import APIRespuesta
from .models import Actividad
from .serializers import ActividadSerializer


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
