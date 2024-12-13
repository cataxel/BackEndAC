from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from BackEndAC.publics.Generics.Respuesta import APIRespuesta
from actividades.models import Grupo, Inscripcion
from actividades.serializers import InscripcionSerializer
from evaluacion.models import Evaluacion, ListaEspera, Asistencia
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