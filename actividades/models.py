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
        app_label = 'actividades'  # Esto le dice a Django que este modelo está en la app 'actividades'

    def __str__(self):
        return f'{self.descripcion} ({self.fecha_inicial} - {self.fecha_final})'

    def tiene_espacio(self):
        """
        Verifica si el grupo tiene espacio disponible para nuevas inscripciones.
        Cuenta las inscripciones que tienen estado 'inscrito' para este grupo.
        """
        # Consulta en la tabla de Inscripcion para obtener el conteo de inscritos
        inscripciones_count = Inscripcion.objects.filter(grupo=self, estado='inscrito').count()

        # Compara el conteo con la capacidad del grupo
        return inscripciones_count < self.capacidad


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

    ESTADO_CHOICES = [
        ('inscrito', 'Inscrito'),
        ('en espera', 'En espera'),
    ]

    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        'usuarios.Usuario', to_field='id', on_delete=models.CASCADE, db_column='usuario_id'
    )
    grupo = models.ForeignKey(
        'actividades.Grupo', to_field='id', on_delete=models.CASCADE, db_column='grupo_id'
    )
    #fecha_inscripcion = models.DateField(auto_now_add=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='en espera',
    )

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        ordering = ['fecha_inscripcion']
        managed = False
        db_table = 'inscripciones'
        app_label = 'inscripciones'

    def __str__(self):
        return f'Inscripción {self.guid} ({self.estado})'


class Participacion(models.Model):
    """
    Modelo que representa las participaciones de los usuarios en las actividades de un grupo.

    Attributes:
        guid (UUIDField): Identificador único de la participación.
        usuario (ForeignKey): ID del usuario que participa.
        grupo (ForeignKey): ID del grupo al que pertenece la participación.
        fecha_participacion (DateTimeField): Fecha y hora de la participación.
    """
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        'usuarios.Usuario', to_field='id', on_delete=models.CASCADE, db_column='usuario_id'
    )
    grupo = models.ForeignKey(
        'actividades.Grupo', to_field='id', on_delete=models.CASCADE, db_column='grupo_id'
    )
    fecha_participacion = models.DateField()
    puntos = models.IntegerField()

    class Meta:
        verbose_name = 'Participación'
        verbose_name_plural = 'Participaciones'
        ordering = ['fecha_participacion']
        managed = False
        db_table = 'participaciones'
        app_label = 'participaciones'

    def __str__(self):
        return f'Participación {self.guid} - Usuario {self.usuario_id}, Grupo {self.grupo_id}'

class Asistencia(models.Model):
    """
    Modelo que representa la asistencia de los usuarios en las actividades de un grupo.

    Attributes:
        guid (UUIDField): Identificador único de la asistencia.
        usuario (ForeignKey): ID del usuario relacionado con la asistencia.
        grupo (ForeignKey): ID del grupo relacionado con la asistencia.
        fecha_registro (DateField): Fecha en la que se registra la asistencia.
        estado (CharField): Estado de la asistencia (presente o ausente).
    """
    ESTADO_CHOICES = [
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
    ]

    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        'usuarios.Usuario', to_field='id', on_delete=models.CASCADE, db_column='usuario_id'
    )
    grupo = models.ForeignKey(
        'actividades.Grupo', to_field='id', on_delete=models.CASCADE, db_column='grupo_id'
    )
    fecha_registro = models.DateField()
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='ausente'
    )

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['fecha_registro']
        managed = False
        db_table = 'asistencia'
        app_label = 'asistencias'

    def __str__(self):
        return f'Asistencia {self.guid} - Usuario {self.usuario_id}, Grupo {self.grupo_id}, Estado {self.estado}'
