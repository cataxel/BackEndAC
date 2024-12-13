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
    usuario_id = serializers.IntegerField(write_only=True)  # Cambiado a IntegerField
    grupo_id = serializers.IntegerField(write_only=True)  # Cambiado a IntegerField

    calificacion = serializers.DecimalField(max_digits=2, decimal_places=1, required=True)
    calificacion_final = serializers.DecimalField(max_digits=2, decimal_places=1, required=False, read_only=True)
    comentarios = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Evaluacion
        fields = ['guid', 'usuario_id', 'grupo_id', 'calificacion', 'calificacion_final', 'comentarios']

    def validate(self, data):
        usuario_id = data.get('usuario_id')
        grupo_id = data.get('grupo_id')

        data['usuario'] = get_object_or_404(Usuario, id=usuario_id)
        data['grupo'] = get_object_or_404(Grupo, id=grupo_id)

        return data

    def calculate_final_grade(self, usuario, grupo, calificacion_docente):
        total_asistencias = Asistencia.objects.filter(grupo=grupo).values('fecha_registro').distinct().count()
        asistencias_usuario = Asistencia.objects.filter(grupo=grupo, usuario=usuario).values('fecha_registro').distinct().count()

        porcentaje_asistencia = (Decimal(asistencias_usuario) / Decimal(total_asistencias)) * Decimal(10) if total_asistencias > 0 else Decimal(0)
        calificacion_docente_final = Decimal(calificacion_docente) * Decimal(0.9)

        calificacion_total = porcentaje_asistencia + calificacion_docente_final
        calificacion_total = min(max(calificacion_total, Decimal(1)), Decimal(100))
        calificacion_total = calificacion_total.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)

        return calificacion_total

    def create(self, validated_data):
        usuario = validated_data.pop('usuario')
        grupo = validated_data.pop('grupo')
        calificacion_docente = validated_data['calificacion']

        validated_data['calificacion_final'] = self.calculate_final_grade(usuario, grupo, calificacion_docente)

        return Evaluacion.objects.create(usuario=usuario, grupo=grupo, **validated_data)

    def update(self, instance, validated_data):
        usuario = validated_data.get('usuario', instance.usuario)
        grupo = validated_data.get('grupo', instance.grupo)
        calificacion_docente = validated_data.get('calificacion', instance.calificacion)

        instance.calificacion_final = self.calculate_final_grade(usuario, grupo, calificacion_docente)

        instance.calificacion = validated_data.get('calificacion', instance.calificacion)
        instance.comentarios = validated_data.get('comentarios', instance.comentarios)
        instance.save()

        return instance
