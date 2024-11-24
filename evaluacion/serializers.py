from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from actividades.models import Actividad
from usuarios.models import Usuario
from .models import Evaluacion, ListaEspera
import uuid

class EvaluacionSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo de Evaluación.

    Convierte las instancias del modelo de Evaluación a representaciones JSON y viceversa.
    """

    guid = serializers.UUIDField(default=uuid.uuid4, read_only=True)
    usuario_id = serializers.UUIDField(source='usuario.guid')  # Usamos 'guid' para representar el usuario
    actividad_id = serializers.UUIDField(source='actividad.guid')  # Usamos 'guid' para representar la actividad
    calificacion = serializers.DecimalField(max_digits=2, decimal_places=1)
    comentarios = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Evaluacion
        fields = ['guid', 'usuario_id', 'actividad_id', 'calificacion', 'comentarios']

    def create(self, validated_data):
        """
        Crea una nueva evaluación a partir de los datos validados.
        """
        # Accedemos directamente al GUID del usuario y de la actividad
        usuario_guid = validated_data['usuario']['guid']
        actividad_guid = validated_data['actividad']['guid']

        try:
            # Buscamos los objetos relacionados por su GUID
            usuario = Usuario.objects.get(guid=usuario_guid)
            actividad = Actividad.objects.get(guid=actividad_guid)
        except Usuario.DoesNotExist:
            raise ValidationError(f"No se encontró el usuario con GUID {usuario_guid}")
        except Actividad.DoesNotExist:
            raise ValidationError(f"No se encontró la actividad con GUID {actividad_guid}")

        # Ahora removemos las claves 'usuario' y 'actividad' de validated_data
        validated_data.pop('usuario', None)
        validated_data.pop('actividad', None)

        # Creamos la instancia de Evaluacion sin pasar los campos duplicados
        evaluacion = Evaluacion.objects.create(
            usuario=usuario,
            actividad=actividad,
            **validated_data  # Pasamos el resto de los datos validados
        )

        return evaluacion

    def update(self, instance, validated_data):
        """
        Actualiza una evaluación existente con los nuevos datos validados.
        """
        # Actualizamos los campos de la instancia existente
        instance.calificacion = validated_data.get('calificacion', instance.calificacion)
        instance.comentarios = validated_data.get('comentarios', instance.comentarios)

        # Guardamos la instancia actualizada
        instance.save()
        return instance

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