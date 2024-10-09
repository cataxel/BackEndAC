from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator
from django.db import models
import uuid

from django.db.models.lookups import Regex
from rest_framework.exceptions import ValidationError

class Roles(models.Model):
    """
    Modelo que representa un rol en el sistema.

    Attributes:
        guid (UUIDField): Identificador único del rol.
        nombre (CharField): Nombre del rol.
        descripcion (TextField): Descripción del rol.
    """

    guid = models.UUIDField(unique=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['nombre']
        managed = False
        db_table = 'roles'

    def save(self, *args, **kwargs):
        """
        Guarda el rol en la base de datos después de validar los datos.
        """
        self.full_clean()
        super().save(*args, **kwargs)

ROLES = [
    {'nombre': 'Estudiante', 'descripcion': 'Rol para estudiantes'},
    {'nombre': 'Docente', 'descripcion': 'Rol para docentes'},
    {'nombre': 'Administración', 'descripcion': 'Rol para administración'},
]

def create_roles(sender, **kwargs):
    """
    Crea roles predeterminados en la base de datos si no existen.

    Args:
        sender: El remitente de la señal.
        **kwargs: Argumentos adicionales.
    """
    for rol in ROLES:
        Roles.objects.get_or_create(nombre=rol['nombre'], defaults={
            'guid': uuid.uuid4(),
            'descripcion': rol['descripcion']
        })

class Usuario(models.Model):
    """
    Modelo que representa un usuario en el sistema.

    Attributes:
        guid (UUIDField): Identificador único del usuario.
        nombre (CharField): Nombre del usuario.
        correo (CharField): Correo electrónico único del usuario.
        contraseña (CharField): Contraseña del usuario.
        rol (ForeignKey): Rol asociado al usuario.
    """

    guid = models.UUIDField(unique=True)
    nombre = models.CharField(max_length=100)
    correo = models.CharField(unique=True, max_length=100)
    contraseña = models.CharField(max_length=255)
    rol = models.ForeignKey(Roles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['correo']),
            models.Index(fields=['rol']),
        ]
        ordering = ['nombre']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        managed = False
        db_table = 'usuarios'

    def __str__(self):
        return self.nombre

    def clean(self):
        """
        Valida los datos del usuario antes de guardarlos.
        """
        email_validator = EmailValidator()
        try:
            email_validator(self.correo)
        except ValidationError:
            raise ValidationError('El correo no es válido')
        if not self.rol:
            raise ValidationError('El usuario debe tener un rol asignado')

    def set_password(self, raw_password: str) -> None:
        """
        Establece la contraseña del usuario.

        Args:
            raw_password (str): La contraseña en texto plano.
        """
        self.contrasena = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """
        Verifica la contraseña del usuario.

        Args:
            raw_password (str): La contraseña en texto plano.

        Returns:
            bool: True si la contraseña es correcta, False en caso contrario.
        """
        return check_password(raw_password, self.contrasena)

    def rol_user(self) -> str:
        """
        Obtiene el nombre del rol del usuario.

        Returns:
            str: Nombre del rol del usuario.
        """
        return self.rol.nombre

    def save(self, *args, **kwargs) -> None:
        """
        Guarda el usuario en la base de datos después de validar los datos.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def find_by_role(cls, role_name: str):
        """
        Encuentra usuarios por nombre de rol.

        Args:
            role_name (str): Nombre del rol.

        Returns:
            QuerySet: Conjunto de usuarios que tienen el rol especificado.
        """
        return cls.objects.filter(rol__nombre=role_name)

    @classmethod
    def find_by_email(cls, email: str):
        """
        Encuentra un usuario por correo electrónico.

        Args:
            email (str): Correo electrónico del usuario.

        Returns:
            Usuario: Instancia del usuario encontrado.
        """
        return cls.objects.get(correo=email)

    @classmethod
    def find_by_id(cls, guid: uuid.UUID):
        """
        Encuentra un usuario por su identificador único.

        Args:
            guid (uuid.UUID): Identificador único del usuario.

        Returns:
            Usuario: Instancia del usuario encontrado.
        """
        return cls.objects.get(guid=guid)

    @classmethod
    def find_all(cls):
        """
        Encuentra todos los usuarios.

        Returns:
            QuerySet: Conjunto de todos los usuarios.
        """
        return cls.objects.all()