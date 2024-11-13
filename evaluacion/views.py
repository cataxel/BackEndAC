from django.shortcuts import render
from rest_framework import viewsets, status

from BackEndAC.publics.Generics.Respuesta import APIRespuesta
from evaluacion.models import Evaluacion
from evaluacion.serializers import EvaluacionSerializer


class EvaluacionViewSet(viewsets.ModelViewSet):
    """
    Vista para manejar las operaciones CRUD de Evaluaciones.
    """
    queryset = Evaluacion.objects.all()  # QuerySet que obtiene todas las evaluaciones
    serializer_class = EvaluacionSerializer  # Serializador que convierte las evaluaciones a JSON y viceversa
    lookup_field = 'guid'

    def create(self, request, *args, **kwargs)  :
        """
        Crea una nueva evaluación.
        """
        try:
            # Usamos el serializador para validar y guardar los datos
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return APIRespuesta(
                    estado=True,
                    mensaje="Evaluación creada con éxito",
                    data=serializer.data,
                    codigoestado=status.HTTP_201_CREATED
                ).to_response()
            else:
                return APIRespuesta(
                    estado=False,
                    mensaje="Error al crear la evaluación",
                    data=serializer.errors,
                    codigoestado=status.HTTP_400_BAD_REQUEST
                ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje=f"Error inesperado",
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

    def retrieve(self, request, *args, **kwargs):
        """
        Obtiene una evaluación específica.
        """
        try:
            evaluacion = self.get_object()  # Obtiene la evaluación GUID
            serializer = self.get_serializer(evaluacion)
            return APIRespuesta(
                estado=True,
                mensaje="Evaluación obtenida con éxito",
                data=serializer.data,
                codigoestado=status.HTTP_200_OK
            ).to_response()
        except Evaluacion.DoesNotExist:
            return APIRespuesta(
                estado=False,
                mensaje="Evaluación no encontrada",
                data=None,
                codigoestado=status.HTTP_404_NOT_FOUND
            ).to_response()

    def update(self, request, *args, **kwargs):
        """
        Actualiza una evaluación existente.
        """
        try:
            # Obtenemos la evaluación a actualizar
            evaluacion = self.get_object()
            # Usamos el serializador para validar y actualizar los datos
            serializer = self.get_serializer(evaluacion, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return APIRespuesta(
                    estado=True,
                    mensaje="Evaluación actualizada con éxito",
                    data=serializer.data,
                    codigoestado=status.HTTP_200_OK
                ).to_response()
            else:
                return APIRespuesta(
                    estado=False,
                    mensaje="Error al actualizar la evaluación",
                    data=serializer.errors,
                    codigoestado=status.HTTP_400_BAD_REQUEST
                ).to_response()
        except Evaluacion.DoesNotExist:
            return APIRespuesta(
                estado=False,
                mensaje="Evaluación no encontrada",
                data=None,
                codigoestado=status.HTTP_404_NOT_FOUND
            ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje=f"Error inesperado",
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

    def destroy(self, request, *args, **kwargs):
        """
        Elimina una evaluación existente.
        """
        try:
            evaluacion = self.get_object()
            evaluacion.delete()
            return APIRespuesta(
                estado=True,
                mensaje="Evaluación eliminada con éxito",
                data=None,
                codigoestado=status.HTTP_204_NO_CONTENT
            ).to_response()
        except Evaluacion.DoesNotExist:
            return APIRespuesta(
                estado=False,
                mensaje="Evaluación no encontrada",
                data=None,
                codigoestado=status.HTTP_404_NOT_FOUND
            ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje=f"Error inesperado",
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()