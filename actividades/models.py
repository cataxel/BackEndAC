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
        fecha_inicio (DateTimeField): Fecha y hora de inicio de la actividad.
        fecha_fin (DateTimeField): Fecha y hora de finalización de la actividad.
    """

    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    capacidad = models.IntegerField()

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['fecha_inicio']
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
