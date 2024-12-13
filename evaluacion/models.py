import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.exceptions import ValidationError


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
        app_label = 'evaluaciones'  # Reemplazar con el nombre de tu    aplicación

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


class Evaluacion(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)  # Relación con el modelo Usuario
    grupo = models.ForeignKey('actividades.Grupo', on_delete=models.CASCADE)  # Relación con el modelo Grupo
    calificacion = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]  # Validaciones para respetar el rango 0 - 5
    )
    calificacion_final = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        blank=True,
        null=True  # Campo opcional para calificación final
    )
    comentarios = models.TextField(blank=True, null=True)  # Comentarios opcionales

    class Meta:
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'
        ordering = ['usuario']  # Ordenar por usuario de forma predeterminada
        managed = False  # Indica que la tabla ya fue creada manualmente
        db_table = 'evaluaciones'  # Nombre de la tabla en la base de datos
        app_label = 'evaluacion'  # Define el módulo de la aplicación para separar modelos

    def __str__(self):
        return f"Evaluación de {self.usuario} en el grupo {self.grupo}"


