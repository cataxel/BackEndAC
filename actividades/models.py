from django.db import models

# Create your models here.
from django.db import models
import uuid

class Actividad(models.Model):
    """
    Modelo que representa una actividad en el sistema.

    Attributes:
        guid (UUIDField): Identificador único de la actividad.
        nombre (CharField): Nombre de la actividad.
        descripcion (TextField): Descripción de la actividad.
    """

    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['nombre']
        managed = False
        db_table = 'actividades'
        app_label = 'actividades'

    def __str__(self):
        return self.nombre

    def delete(self, *args, **kwargs):
        """
        Elimina la actividad de la base de datos.
        """
        super().delete(*args, **kwargs)





class Grupo(models.Model):
    """
    Modelo que representa un grupo en el sistema.

    Attributes:
        guid (UUIDField): Identificador único del grupo.
        descripcion (TextField): Descripción del grupo.
        ubicacion (TextField): Descripción del grupo.
        hora_inicial (TimeField): Hora inicial del grupo.
        hora_final (TimeField): Hora final del grupo.
        fecha_inicial (DateField): Fecha inicial del grupo.
        fecha_final (DateField): Fecha final del grupo.
        capacidad (IntegerField): Capacidad del grupo.
        usuario (ForeignKey): Referencia al usuario creador o responsable del grupo.
        actividad (ForeignKey): Referencia a la actividad relacionada con el grupo.
    """

    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    descripcion = models.TextField()
    ubicacion = models.TextField()
    hora_inicial = models.TimeField()
    hora_final = models.TimeField()
    fecha_inicial = models.DateField()
    fecha_final = models.DateField()
    capacidad = models.IntegerField()

    usuario = models.ForeignKey(
        'usuarios.Usuario',  # Asume que tienes un modelo Usuario
        to_field='id',
        on_delete=models.CASCADE,
        db_column='usuario_id'
    )
    actividad = models.ForeignKey(
        'actividades.Actividad',
        to_field='id',
        on_delete=models.CASCADE,
        db_column='actividad_id'
    )

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['fecha_inicial']
        managed = False
        db_table = 'grupos'
        app_label = 'grupos'

    def __str__(self):
        return f'{self.descripcion} ({self.fecha_inicial} - {self.fecha_final})'





class Inscripcion(models.Model):
    """
    Modelo que representa una inscripción a un grupo en el sistema.

    Attributes:
        guid (UUIDField): Identificador único de la inscripción.
        usuario (IntegerField): ID del usuario inscrito.
        grupo (IntegerField): ID del grupo a la que el usuario se inscribe.
        fecha_inscripcion (DateField): Fecha de inscripción.
        estado (CharField): Estado de la inscripción (por ejemplo, 'pendiente', 'confirmada').
    """

    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        'usuarios.Usuario', to_field='id', on_delete=models.CASCADE, db_column='usuario_id'
    )
    grupo = models.ForeignKey(
        'grupos.Grupo', to_field='id', on_delete=models.CASCADE, db_column='grupo_id'
    )
    #fecha_inscripcion = models.DateField(auto_now_add=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        ordering = ['fecha_inscripcion']
        managed = False
        db_table = 'inscripciones'
        app_label = 'inscripciones'

    def __str__(self):
        return f'Inscripción {self.guid}'


