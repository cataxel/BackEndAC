# Create your views here.
from logging import fatal

from rest_framework import generics, viewsets, status, serializers
from rest_framework.exceptions import NotFound
from rest_framework.fields import empty

from BackEndAC.publics.Generics.Respuesta import APIRespuesta
from .models import Actividad, Grupo, Inscripcion, Participacion, Asistencia
from .serializers import ActividadSerializer, GrupoSerializer, InscripcionSerializer, ParticipacionSerializer, \
    AsistenciaSerializer


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

    def validate_name(self, name, guid):
        actividades = Actividad.objects.filter(nombre=name)
        for actividad in actividades:
            if actividad.guid != guid:
                if actividad.nombre == name:
                    return False
        return True


    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                if not self.validate_name(serializer.validated_data['nombre'], empty):
                    return APIRespuesta(
                        estado=False,
                        mensaje='Esa actividad ya existe',
                        codigoestado=status.HTTP_406_NOT_ACCEPTABLE
                    ).to_response()
                print("hola")
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
                guid = request.data.get('guid', self.get_object().guid)

                if not self.validate_name(serializer.validated_data['nombre'], guid):
                    return APIRespuesta(
                        estado=False,
                        mensaje='Esa actividad ya existe',
                        codigoestado=status.HTTP_406_NOT_ACCEPTABLE
                    ).to_response()

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




from datetime import datetime
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
                mensaje='Grupo no encontrada',
                codigoestado=status.HTTP_404_NOT_FOUND
            ).to_response()
        except Exception as e:
            return APIRespuesta(
                estado=False,
                mensaje=f'Error inesperado',
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

    MAX_CAPACITY = 50  # Máxima capacidad permitida

    def validate_date_time_conflict(self, fecha_inicial, fecha_final, hora_inicial, hora_final, ubicacion, guid):
        # Convertir las horas a objetos datetime.time
        hora_inicial = datetime.strptime(hora_inicial, "%H:%M:%S").time()
        hora_final = datetime.strptime(hora_final, "%H:%M:%S").time()

        # Validar si ya existe un grupo en la misma ubicación que se solape con las fechas y/o las horas
        conflicting_groups = Grupo.objects.filter(
            ubicacion=ubicacion,
            fecha_inicial__lte=fecha_final,
            fecha_final__gte=fecha_inicial
        )

        for group in conflicting_groups:
            if group.guid != guid:
                if hora_inicial < group.hora_final and hora_final > group.hora_inicial:
                    return False
        return True

    def validate_user_role(self, user):
        # Validación de rol del usuario
        rol = str(user.rol)
        return rol in ["Estudiante"] # Ajusta los roles según tu modelo

    def validate_capacity(self, capacidad):
        # Validar que la capacidad no exceda el límite
        if capacidad > self.MAX_CAPACITY:
            return False
        return True

    def validate_dates(self, fecha_inicial, fecha_final, hora_inicial, hora_final):
        # Obtener la fecha y hora actuales
        fecha_actual = datetime.now()
        # Formatear la fecha actual a "YYYY-MM-DD"
        fechaActual_formateada = fecha_actual.strftime("%Y-%m-%d")

        if fecha_final < fecha_inicial or fecha_inicial < fechaActual_formateada or hora_inicial > hora_final:
            return False
        return True

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Recoger los datos del request
                fecha_inicial = request.data.get('fecha_inicial')
                fecha_final = request.data.get('fecha_final')
                hora_inicial = request.data.get('hora_inicial')
                hora_final = request.data.get('hora_final')
                ubicacion = request.data.get('ubicacion')
                usuario = request.data.get('usuario')

                # Validaciones
                if not self.validate_user_role(Usuario.objects.get(guid=usuario)):
                    return APIRespuesta(
                        estado=False,
                        mensaje='El usuario no puede ser asignado al grupo',
                        codigoestado=status.HTTP_403_FORBIDDEN
                    ).to_response()

                if not self.validate_dates(fecha_inicial, fecha_final, hora_inicial, hora_final):
                    return APIRespuesta(
                        estado=False,
                        mensaje='La fecha y hora no es valida',
                        codigoestado=status.HTTP_400_BAD_REQUEST
                    ).to_response()

                if not self.validate_date_time_conflict(fecha_inicial, fecha_final, hora_inicial, hora_final, ubicacion, empty):
                    return APIRespuesta(
                        estado=False,
                        mensaje='El grupo se solapa con otro en la misma ubicación en esas fechas y horas',
                        codigoestado=status.HTTP_400_BAD_REQUEST
                    ).to_response()

                if not self.validate_capacity(request.data.get('capacidad')):
                    return APIRespuesta(
                        estado=False,
                        mensaje='La capacidad excede el límite permitido',
                        codigoestado=status.HTTP_400_BAD_REQUEST
                    ).to_response()



                # Si todo está bien, se crea el grupo
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
                mensaje=f'Error inesperado: {str(e)}',
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

    def update(self, request, *args, **kwargs):
        try:
            # Obtener el objeto que se va a actualizar
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                # Recoger los datos del request
                fecha_inicial = request.data.get('fecha_inicial', instance.fecha_inicial)
                fecha_final = request.data.get('fecha_final', instance.fecha_final)
                hora_inicial = request.data.get('hora_inicial', instance.hora_inicial)
                hora_final = request.data.get('hora_final', instance.hora_final)
                ubicacion = request.data.get('ubicacion', instance.ubicacion)
                guid = request.data.get('guid', instance.guid)
                usuario = request.data.get('usuario', instance.usuario.guid)

                # Validaciones
                if not self.validate_user_role(Usuario.objects.get(guid=usuario)):
                    return APIRespuesta(
                        estado=False,
                        mensaje='El usuario no puede ser asignado al grupo',
                        codigoestado=status.HTTP_403_FORBIDDEN
                    ).to_response()

                if not self.validate_dates(fecha_inicial, fecha_final, hora_inicial, hora_final):
                    return APIRespuesta(
                        estado=False,
                        mensaje='La fecha y hora no es válida',
                        codigoestado=status.HTTP_400_BAD_REQUEST
                    ).to_response()

                if not self.validate_date_time_conflict(fecha_inicial, fecha_final, hora_inicial, hora_final,
                                                        ubicacion, guid):
                    return APIRespuesta(
                        estado=False,
                        mensaje='El grupo se solapa con otro en la misma ubicación en esas fechas y horas',
                        codigoestado=status.HTTP_400_BAD_REQUEST
                    ).to_response()

                if not self.validate_capacity(request.data.get('capacidad', instance.capacidad)):
                    return APIRespuesta(
                        estado=False,
                        mensaje='La capacidad excede el límite permitido',
                        codigoestado=status.HTTP_400_BAD_REQUEST
                    ).to_response()

                # Si todo está bien, se actualiza el grupo
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
                mensaje=f'Error inesperado: {str(e)}',
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

class ParticipacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar las participaciones de usuarios en los grupos.
    Soporta operaciones CRUD: listar, recuperar, crear, actualizar y eliminar participaciones.
    """
    serializer_class = ParticipacionSerializer
    queryset = Participacion.objects.all()
    lookup_field = 'guid'  # Utiliza `guid` como identificador para las operaciones.

    def perform_create(self, serializer):
        """
        Personaliza la creación de una nueva participación, como generar un GUID o realizar validaciones adicionales.
        """
        usuario = serializer.validated_data.get('usuario')
        print(usuario.rol)
        if str(usuario.rol) != "Estudiante":  # Cambia 'rol' si el campo del modelo tiene otro nombre
            raise serializers.ValidationError("La asistencia solo puede registrarse a usuarios con el rol de Estudiante.")
        # Aquí puedes agregar lógica adicional antes de guardar
        serializer.save()


class AsistenciaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar la asistencia de usuarios en los grupos.
    Soporta operaciones CRUD: listar, recuperar, crear, actualizar y eliminar asistencias.
    """
    serializer_class = AsistenciaSerializer
    queryset = Asistencia.objects.all()
    lookup_field = 'guid'  # Utiliza `guid` como identificador para las operaciones.

    def perform_create(self, serializer):
        """
        Personaliza la creación de una nueva asistencia, incluyendo validaciones adicionales.
        Por ejemplo: evitar entradas duplicadas en la misma fecha para un usuario y grupo.
        """
        fecha = serializer.validated_data.get('fecha_registro')
        usuario = serializer.validated_data.get('usuario')
        grupo = serializer.validated_data.get('grupo')

        # Validación: Verificar si ya existe una asistencia para el mismo usuario, grupo y fecha
        if Asistencia.objects.filter(usuario=usuario, grupo=grupo, fecha_registro=fecha).exists():
            raise serializers.ValidationError("Ya existe un registro de asistencia para este usuario en esta fecha.")

        if usuario.rol != "Estudiante":  # Cambia 'rol' si el campo del modelo tiene otro nombre
            raise serializers.ValidationError("La asistencia solo puede registrarse a usuarios con el rol de Estudiante.")

        serializer.save()