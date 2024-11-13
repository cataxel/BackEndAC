from datetime import datetime
from rest_framework import serializers
from .models import Actividad, Inscripcion
from usuarios.models import Usuario

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'

class InscripcionSerializer(serializers.ModelSerializer):
    guid = serializers.CharField(read_only=True)
    # Utilizamos SlugRelatedField para representar el campo guid en lugar del id
    usuario = serializers.SlugRelatedField(
        queryset=Usuario.objects.all(), slug_field='guid', write_only=True
    )
    actividad = serializers.SlugRelatedField(
        queryset=Actividad.objects.all(), slug_field='guid', write_only=True
    )
    # Campos de solo lectura para mostrar el nombre del usuario y la actividad en la respuesta
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    actividad_nombre = serializers.CharField(source='actividad.nombre', read_only=True)

    class Meta:
        model = Inscripcion
        fields = '__all__'