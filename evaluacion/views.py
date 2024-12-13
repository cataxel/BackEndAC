from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from BackEndAC.publics.Generics.Respuesta import APIRespuesta
from actividades.models import Grupo, Inscripcion
from actividades.serializers import InscripcionSerializer
from evaluacion.models import Evaluacion, ListaEspera
from evaluacion.serializers import EvaluacionSerializer, ListaEsperaSerializer


class ListaEsperaViewSet(viewsets.ModelViewSet):
    queryset = ListaEspera.objects.all()
    serializer_class = ListaEsperaSerializer
    lookup_field = 'guid'

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                usuario = serializer.validated_data.get('usuario')
                actividad = serializer.validated_data.get('actividad')

                # Verificar si ya está inscrito o en lista de espera
                if Inscripcion.objects.filter(usuario=usuario, grupo__actividad=actividad).exists():
                    return APIRespuesta(
                        estado=False,
                        mensaje="El usuario ya está inscrito en un grupo de esta actividad.",
                        codigoestado=status.HTTP_400_BAD_REQUEST
                    ).to_response()

                if ListaEspera.objects.filter(usuario=usuario, actividad=actividad).exists():
                    return APIRespuesta(
                        estado=False,
                        mensaje="El usuario ya está en la lista de espera de esta actividad.",
                        codigoestado=status.HTTP_400_BAD_REQUEST
                    ).to_response()

                # Verificar capacidad del grupo relacionado
                grupo = Grupo.objects.filter(actividad=actividad).first()
                if grupo and grupo.tiene_espacio():
                    # Registrar directamente si hay espacio
                    inscripcion = Inscripcion.objects.create(usuario=usuario, grupo=grupo)
                    return APIRespuesta(
                        estado=True,
                        mensaje="Usuario inscrito directamente al grupo.",
                        data= InscripcionSerializer(inscripcion).data,
                        codigoestado=status.HTTP_201_CREATED
                    ).to_response()

                # Si no hay espacio, añadir a la lista de espera
                serializer.save()
                return APIRespuesta(
                    estado=True,
                    mensaje="Usuario agregado a la lista de espera.",
                    data=serializer.data,
                    codigoestado=status.HTTP_201_CREATED
                ).to_response()
            else:
                return APIRespuesta(
                    estado=False,
                    mensaje="Datos inválidos para la lista de espera.",
                    data=serializer.errors,
                    codigoestado=status.HTTP_400_BAD_REQUEST
                ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje="Error inesperado.",
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

class EvaluacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar las evaluaciones.
    """
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    lookup_field = 'guid'  # Utilizamos GUID como identificador en las rutas

    def create(self, request, *args, **kwargs):
        """
        Maneja la lógica para crear evaluaciones y estructura la respuesta con APIRespuesta.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)  # Guarda la evaluación
            return APIRespuesta(
                estado=True,
                mensaje="Evaluación creada exitosamente.",
                data=serializer.data,  # Devolvemos la evaluación creada
                codigoestado=status.HTTP_201_CREATED
            ).to_response()
        except ValidationError as e:
            return APIRespuesta(
                estado=False,
                mensaje="Error al crear la evaluación.",
                data={"errores": e.detail},  # Detalle del error
                codigoestado=status.HTTP_400_BAD_REQUEST
            ).to_response()

    def update(self, request, *args, **kwargs):
        """
        Maneja la lógica para actualizar evaluaciones y estructura la respuesta con APIRespuesta.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)  # Actualiza la evaluación
            return APIRespuesta(
                estado=True,
                mensaje="Evaluación actualizada exitosamente.",
                data=serializer.data,  # Devolvemos la evaluación actualizada
                codigoestado=status.HTTP_200_OK
            ).to_response()
        except ValidationError as e:
            return APIRespuesta(
                estado=False,
                mensaje="Error al actualizar la evaluación.",
                data={"errores": e.detail},  # Detalle del error
                codigoestado=status.HTTP_400_BAD_REQUEST
            ).to_response()

    def destroy(self, request, *args, **kwargs):
        """
        Maneja la lógica para eliminar evaluaciones y estructura la respuesta con APIRespuesta.
        """
        instance = self.get_object()
        try:
            self.perform_destroy(instance)  # Elimina la evaluación
            return APIRespuesta(
                estado=True,
                mensaje="Evaluación eliminada exitosamente.",
                codigoestado=status.HTTP_204_NO_CONTENT
            ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje="Error al eliminar la evaluación.",
                data={"errores": str(e)},  # Detalle del error
                codigoestado=status.HTTP_400_BAD_REQUEST
            ).to_response()

    def list(self, request, *args, **kwargs):
        """
        Recupera todas las evaluaciones y estructura la respuesta con APIRespuesta.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return APIRespuesta(
            estado=True,
            mensaje="Lista de evaluaciones recuperada exitosamente.",
            data=serializer.data,
            codigoestado=status.HTTP_200_OK
        ).to_response()

    def retrieve(self, request, *args, **kwargs):
        """
        Recupera una evaluación específica y estructura la respuesta con APIRespuesta.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return APIRespuesta(
            estado=True,
            mensaje="Evaluación recuperada exitosamente.",
            data=serializer.data,
            codigoestado=status.HTTP_200_OK
        ).to_response()
