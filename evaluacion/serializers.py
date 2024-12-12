from .models import ListaEspera, Evaluacion, Asistencia
from rest_framework.exceptions import ValidationError
from actividades.models import Actividad, Grupo
from usuarios.models import Usuario
from rest_framework import serializers
import uuid

class ListaEsperaSerializer(serializers.ModelSerializer):
    guid = serializers.UUIDField(default=uuid.uuid4(), read_only=True)
    usuario_id = serializers.UUIDField(source='usuario.guid')
    actividad_id = serializers.UUIDField(source='actividad.guid')
    fecha_registro = serializers.DateField()

    class Meta:
        model = ListaEspera
        fields = ['guid', 'usuario_id', 'actividad_id', 'fecha_registro']

    def create(self, validated_data):
        usuario_guid = validated_data.pop('usuario')
        actividad_guid = validated_data.pop('actividad')

        try:
            usuario = ListaEspera.find_by_user(user_guid=usuario_guid)
            actividad = ListaEspera.find_by_activity(activity_guid=actividad_guid)
        except Usuario.DoesNotExist:
            raise ValidationError(f"No se encontro el usuario con GUID {usuario_guid}")
        except Actividad.DoesNotExist:
            raise ValidationError(f"No se encontro la actividad con GUID {actividad_guid}")

        lista_espera = ListaEspera(**validated_data,usuario=usuario,actividad=actividad)
        lista_espera.guid = uuid.uuid4()
        #lista_espera.fecha_registro = validated_data.get('fecha_registro')
        lista_espera.save()
        return lista_espera

class EvaluacionSerializer(serializers.ModelSerializer):
    guid = serializers.UUIDField(default=uuid.uuid4, read_only=True)
    usuario_id = serializers.UUIDField(source='usuario.guid')
    grupo_id = serializers.UUIDField(source='grupo.guid')
    calificacion = serializers.DecimalField(max_digits=2, decimal_places=1, required=False)
    comentarios = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Evaluacion
        fields = ['guid', 'usuario_id', 'grupo_id', 'calificacion', 'comentarios']

    def validate(self, data):
        """
        Validación de asistencia antes de crear o actualizar la evaluación.
        """
        usuario_guid = data['usuario']['guid']
        grupo_guid = data['grupo']['guid']

        try:
            # Verificamos que el usuario tenga al menos el 80% de asistencias
            evaluacion_instance = Evaluacion(usuario_id=usuario_guid, grupo_id=grupo_guid)
            evaluacion_instance.validacion_asistencias()

        except ValidationError as e:
            raise e  # Si no cumple con las asistencias, lanzamos un error

        return data