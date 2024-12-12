from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError

from BackEndAC.publics.Generics.Respuesta import APIRespuesta
from evaluacion.models import Evaluacion, ListaEspera, Asistencia
from evaluacion.serializers import EvaluacionSerializer, ListaEsperaSerializer

class ListaEsperaViewSet(viewsets.ModelViewSet):
    queryset = ListaEspera.objects.all()
    serializer_class = ListaEsperaSerializer
    lookup_field = 'guid'

    def create(self, request, *args, **kwargs):
        try:
            serializer = ListaEsperaSerializer(data=request.data)
            if serializer.is_valid():
                return APIRespuesta(
                    estado = True,
                    mensaje = "Registro en lista de espera exitoso",
                    data = serializer.data,
                    codigoestado = status.HTTP_201_CREATED
                ).to_response()
            else:
                return APIRespuesta(
                    estado = False,
                    mensaje="Error al crear registro en lista de espera",
                    data=serializer.errors,
                    codigoestado=status.HTTP_400_BAD_REQUEST
                ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado = False,
                mensaje = f"Error inesperado",
                data = str(e),
                codigoestado = status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

class EvaluacionViewSet(viewsets.ModelViewSet):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    lookup_field = 'guid'

    def create(self, request, *args, **kwargs):
        # Usamos el serializador para validar los datos de la solicitud
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                # Guardamos los datos si son válidos
                serializer.save()
                return APIRespuesta(
                    estado=True,
                    mensaje="Evaluación creada con éxito",
                    data=serializer.data,
                    codigoestado=status.HTTP_201_CREATED
                ).to_response()
            except ValidationError as e:
                # Si ocurre una validación incorrecta, devolvemos el mensaje de error
                return APIRespuesta(
                    estado=False,
                    mensaje=str(e),
                    data=None,
                    codigoestado=status.HTTP_400_BAD_REQUEST
                ).to_response()
        # Si el serializador no es válido, devolvemos los errores
        return APIRespuesta(
            estado=False,
            mensaje="Datos inválidos",
            data=serializer.errors,
            codigoestado=status.HTTP_400_BAD_REQUEST
        ).to_response()