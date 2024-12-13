from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from rest_framework.generics import get_object_or_404

from .models import ListaEspera, Evaluacion
from rest_framework.exceptions import ValidationError
from actividades.models import Actividad, Grupo, Asistencia, Participacion
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
    usuario_id = serializers.UUIDField(write_only=True)  # GUID del usuario proporcionado
    grupo_id = serializers.UUIDField(write_only=True)  # GUID del grupo proporcionado

    calificacion = serializers.DecimalField(max_digits=2, decimal_places=1, required=True)
    calificacion_final = serializers.DecimalField(max_digits=2, decimal_places=1, required=False, read_only=True)
    comentarios = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Evaluacion
        fields = ['guid', 'usuario_id', 'grupo_id', 'calificacion', 'calificacion_final', 'comentarios']

    def validate(self, data):
        """
        Validación personalizada para asegurarse de que existan los objetos relacionados.
        """
        usuario_guid = data.get('usuario_id')
        grupo_guid = data.get('grupo_id')

        # Resolver el usuario y el grupo
        data['usuario'] = get_object_or_404(Usuario, guid=usuario_guid)
        data['grupo'] = get_object_or_404(Grupo, guid=grupo_guid)

        return data

    def calculate_final_grade(self, usuario, grupo, calificacion_docente):
        """
        Calcula la calificación final basada en asistencias, participaciones y calificación del docente.
        """
        # Obtener el total de fechas únicas de asistencia en el grupo
        total_asistencias = Asistencia.objects.filter(grupo=grupo).values('fecha_registro').distinct().count()

        # Obtener total de asistencias únicas del usuario (fechas únicas)
        asistencias_usuario = Asistencia.objects.filter(grupo=grupo, usuario=usuario).values(
            'fecha_registro').distinct().count()

        # Calcular el porcentaje de asistencia (10% de la calificación)
        porcentaje_asistencia = (Decimal(asistencias_usuario) / Decimal(total_asistencias)) * Decimal(
            10) if total_asistencias > 0 else Decimal(0)

        # Calificación docente (90% de la calificación)
        calificacion_docente_final = Decimal(calificacion_docente) * Decimal(0.9)

        # Calcular calificación total
        calificacion_total = porcentaje_asistencia + calificacion_docente_final

        # Asegurarnos de que esté dentro del rango 1-100
        calificacion_total = min(max(calificacion_total, Decimal(1)), Decimal(100))

        # Redondear a un decimal con ROUND_HALF_UP
        calificacion_total = calificacion_total.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)

        return calificacion_total

    def create(self, validated_data):
        # Extraer el usuario y grupo resueltos
        usuario = validated_data.pop('usuario')
        grupo = validated_data.pop('grupo')
        calificacion_docente = validated_data['calificacion']

        # Calcular la calificación final
        validated_data['calificacion_final'] = self.calculate_final_grade(usuario, grupo, calificacion_docente)

        # Crear la evaluación con los datos
        return Evaluacion.objects.create(usuario=usuario, grupo=grupo, **validated_data)

    def update(self, instance, validated_data):
        # Extraer el usuario y grupo resueltos
        usuario = validated_data.get('usuario', instance.usuario)
        grupo = validated_data.get('grupo', instance.grupo)
        calificacion_docente = validated_data.get('calificacion', instance.calificacion)

        # Calcular la calificación final
        instance.calificacion_final = self.calculate_final_grade(usuario, grupo, calificacion_docente)

        # Actualizar los demás campos
        instance.calificacion = validated_data.get('calificacion', instance.calificacion)
        instance.comentarios = validated_data.get('comentarios', instance.comentarios)
        instance.save()

        return instance
