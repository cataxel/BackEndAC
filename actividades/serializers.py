from datetime import datetime
from rest_framework import serializers
from .models import Actividad, Grupo, Inscripcion, Participacion, Asistencia
from usuarios.models import Usuario

class ActividadSerializer(serializers.ModelSerializer):
    guid = serializers.CharField(read_only=True)

    class Meta:
        model = Actividad
        fields = '__all__'

class GrupoSerializer(serializers.ModelSerializer):
    guid = serializers.CharField(read_only=True)

    # Utilizamos SlugRelatedField para representar el campo guid en lugar del id
    usuario = serializers.SlugRelatedField(
        queryset=Usuario.objects.all(), slug_field='guid', write_only=True
    )
    actividad = serializers.SlugRelatedField(
        queryset=Actividad.objects.all(), slug_field='guid', write_only=True
    )
    # Campos de solo lectura para mostrar el nombre del usuario y el grupo en la respuesta
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    actividad_descripcion = serializers.CharField(source='actividad.nombre', read_only=True)

    class Meta:
        model = Grupo
        fields = '__all__'

class InscripcionSerializer(serializers.ModelSerializer):
    guid = serializers.CharField(read_only=True)
    # Utilizamos SlugRelatedField para representar el campo guid en lugar del id
    usuario = serializers.SlugRelatedField(
        queryset=Usuario.objects.all(), slug_field='guid', write_only=True
    )
    grupo = serializers.SlugRelatedField(
        queryset=Grupo.objects.all(), slug_field='guid', write_only=True
    )
    # Campos de solo lectura para mostrar el nombre del usuario y el grupo en la respuesta
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    grupo_descripcion = serializers.CharField(source='grupo.descripcion', read_only=True)

    estado_label = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = Inscripcion
        fields = '__all__'

    def validate(self, data):
        grupo = data['grupo']

        # Verifica si el grupo tiene espacio para inscripciones
        if not grupo.tiene_espacio():
            raise serializers.ValidationError("El grupo está lleno. El usuario será añadido a la lista de espera.")
        return data

class ParticipacionSerializer(serializers.ModelSerializer):
    guid = serializers.CharField(read_only=True)
    # Utilizamos SlugRelatedField para trabajar con los GUID en lugar del ID
    usuario = serializers.SlugRelatedField(
        queryset=Usuario.objects.all(), slug_field='guid', write_only=True
    )
    grupo = serializers.SlugRelatedField(
        queryset=Grupo.objects.all(), slug_field='guid', write_only=True
    )
    # Campos solo de lectura para mostrar información adicional
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    grupo_descripcion = serializers.CharField(source='grupo.descripcion', read_only=True)

    class Meta:
        model = Participacion
        fields = '__all__'

    def validate(self, data):
        """
        Validación de rango de fechas para la participación.
        La fecha de participación debe estar dentro del rango de fechas del grupo.
        """
        grupo = data['grupo']
        usuario = data['usuario']
        fecha_participacion = data.get('fecha_participacion')  # Ajusta si este campo es diferente

        # Validar que la fecha de participación esté dentro del rango de fechas del grupo
        if not (grupo.fecha_inicial <= fecha_participacion <= grupo.fecha_final):
            raise serializers.ValidationError(
                "La fecha de participación debe estar dentro del rango de fechas del grupo."
            )

        return data


class AsistenciaSerializer(serializers.ModelSerializer):
    guid = serializers.CharField(read_only=True)
    # Utilizamos SlugRelatedField para trabajar con GUID
    usuario = serializers.SlugRelatedField(
        queryset=Usuario.objects.all(), slug_field='guid', write_only=True
    )
    grupo = serializers.SlugRelatedField(
        queryset=Grupo.objects.all(), slug_field='guid', write_only=True
    )
    # Agregar el estado como etiqueta legible (`presente` o `ausente`)
    estado_label = serializers.CharField(source='get_estado_display', read_only=True)
    # Campos de solo lectura
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    grupo_descripcion = serializers.CharField(source='grupo.descripcion', read_only=True)

    class Meta:
        model = Asistencia
        fields = '__all__'

    def validate_fecha_registro(self, value):
        # Validar que la fecha de registro no sea futura
        if value > datetime.today().date():
            raise serializers.ValidationError("La fecha de registro no puede estar en el futuro.")
        return value
