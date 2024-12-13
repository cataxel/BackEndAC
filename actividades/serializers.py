from datetime import datetime
from rest_framework import serializers
from .models import Actividad, Grupo, Inscripcion
from usuarios.models import Usuario

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'

class GrupoSerializer(serializers.ModelSerializer):
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