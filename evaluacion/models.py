from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid

class Evaluacion(models.Model):
    """
    Modelo que representa una evaluación de una actividad por un usuario en el sistema.

    Attributes:
        guid (UUIDField): Identificador único de la evaluación.
        usuario (ForeignKey): Usuario que realiza la evaluación.
        actividad (ForeignKey): Actividad que está siendo evaluada.
        calificacion (Decimal): Calificación otorgada a la actividad (entre 0 y 5).
        comentarios (TextField): Comentarios sobre la actividad.
    """

    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    actividad = models.ForeignKey('actividades.Actividad', on_delete=models.CASCADE)
    calificacion = models.DecimalField(max_digits=2, decimal_places=1, validators=[
        MinValueValidator(0), MaxValueValidator(5)])
    comentarios = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['usuario']),
            models.Index(fields=['actividad']),
            models.Index(fields=['calificacion']),
        ]
        ordering = ['usuario', 'actividad']
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'
        managed = False  # Si no deseas que Django cree o migre la tabla, usa managed = False
        db_table = 'evaluaciones'
        app_label = 'evaluaciones'

    def __str__(self):
        return f'Evaluación de {self.usuario} para {self.actividad}'

    def save(self, *args, **kwargs):
        """
        Guarda la evaluación en la base de datos después de realizar cualquier validación.
        """
        self.full_clean()  # Validar antes de guardar
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Elimina la evaluación de la base de datos.
        """
        super().delete(*args, **kwargs)

    @classmethod
    def find_by_user(cls, user_guid: uuid.UUID):
        """
        Encuentra todas las evaluaciones realizadas por un usuario específico.

        Args:
            user_guid (uuid.UUID): El identificador único del usuario.

        Returns:
            QuerySet: Conjunto de evaluaciones realizadas por el usuario.
        """
        return cls.objects.filter(usuario__guid=user_guid)

    @classmethod
    def find_by_activity(cls, activity_guid: uuid.UUID):
        """
        Encuentra todas las evaluaciones realizadas sobre una actividad específica.

        Args:
            activity_guid (uuid.UUID): El identificador único de la actividad.

        Returns:
            QuerySet: Conjunto de evaluaciones realizadas sobre la actividad.
        """
        return cls.objects.filter(actividad__guid=activity_guid)

    @classmethod
    def find_by_calificacion(cls, calificacion: float):
        """
        Encuentra evaluaciones con una calificación específica.

        Args:
            calificacion (float): La calificación que se busca.

        Returns:
            QuerySet: Conjunto de evaluaciones con la calificación especificada.
        """
        return cls.objects.filter(calificacion=calificacion)

class ListaEspera(models.Model):
    """
    Modelo que representa una lista de espera en la base de datos.

    Este modelo se utiliza para gestionar la información de usuarios en listas de espera
    para diversas actividades. Incluye campos para el identificador único (GUID) del usuario,
    la actividad para la cual el usuario está en la lista de espera y la fecha de registro
    de la entrada en la lista de espera.
    """
    guid = models.UUIDField(unique=True, default=uuid.uuid4(),editable=False)
    usuario = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE)
    actividad = models.ForeignKey('actividades.Actividad',on_delete=models.CASCADE)
    fecha_registro = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=['usuario']),
            models.Index(fields=['actividad']),
        ]
        ordering = ['usuario', 'actividad']
        verbose_name = 'Lista de Espera'
        verbose_name_plural = 'Listas de Espera'
        managed = False  # Para que Django no cree o migre la tabla
        db_table = 'Listas_Espera'  # Nombre de la tabla en la base de datos
        app_label = 'evaluaciones'  # Reemplazar con el nombre de tu aplicación

    def __str__(self):
        return f'Lista de Espera para {self.usuario} en {self.actividad}'

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Elimina al usuario de la lista de espera en la base de datos.
        """
        super().delete(*args, **kwargs)

    @classmethod
    def find_by_user(cls, user_guid: uuid.UUID):
        """
        Finds and returns queryset based on the provided user GUID.

        Args:
            cls: The class itself.
            user_guid (uuid.UUID): The unique identifier of the user.

        Returns:
            QuerySet: The queryset matching the user GUID.
        """
        return cls.objects.filter(usuario__guid=user_guid)

    @classmethod
    def find_by_activity(cls, activity_guid: uuid.UUID):
        """
        Class method to find records based on the given activity GUID.

        Arguments:
            activity_guid (uuid.UUID): The GUID of the activity to filter records.

        Returns:
            QuerySet: A queryset containing records that match the given activity GUID.
        """
        return cls.objects.filter(actividad__guid=activity_guid)
