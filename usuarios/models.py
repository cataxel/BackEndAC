from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import EmailValidator
from django.db import models
import uuid

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
        app_label = 'usuarios'

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
    rol = models.ForeignKey(Roles,to_field='id',on_delete=models.CASCADE)


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
        app_label = 'usuarios'

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
        self.contraseña = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """
        Verifica la contraseña del usuario.

        Args:
            raw_password (str): La contraseña en texto plano.

        Returns:
            bool: True si la contraseña es correcta, False en caso contrario.
        """
        return check_password(raw_password, self.contraseña)

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

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)  # Llama al metodo delete de la clase padre

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

class Perfil(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # GUID único
    usuario = models.ForeignKey(
        'Usuario', to_field='id', on_delete=models.CASCADE, db_column='usuario_id'
    )  # Relación con la tabla Usuarios
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Teléfono opcional
    direccion = models.TextField(blank=True, null=True)  # Dirección opcional
    carrera = models.TextField(blank=True, null=True)  # Carrera opcional
    numero_control = models.IntegerField(unique=True)  # Número de control único

    class Meta:
        indexes = [
            models.Index(fields=['usuario']),  # Índice sobre usuario_id
            models.Index(fields=['numero_control']),  # Índice sobre numero_control
        ]
        ordering = ['usuario']
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        managed = False  # Para indicar que la tabla ya está creada en la BD
        db_table = 'perfiles'  # Nombre de la tabla en la base de datos
        app_label = 'usuarios'

    def __str__(self):
        """Representación en texto del objeto Perfil."""
        return f'Perfil: {self.usuario} (Control: {self.numero_control})'

    # Metodo para actualizar el teléfono
    def actualizar_telefono(self, nuevo_telefono):
        """Actualiza el teléfono del perfil."""
        self.telefono = nuevo_telefono
        self.save()

    # Metodo para validar si tiene carrera asignada
    def tiene_carrera(self):
        """Devuelve True si el perfil tiene carrera asignada."""
        return bool(self.carrera)

    # Metodo para obtener dirección abreviada
    def direccion_abreviada(self):
        """Devuelve los primeros 30 caracteres de la dirección."""
        return self.direccion[:30] + '...' if self.direccion and len(self.direccion) > 30 else self.direccion

    # Metodo de búsqueda por número de control (classmethod)
    @classmethod
    def buscar_por_numero_control(cls, numero_control):
        """Busca un perfil por su número de control."""
        return cls.objects.filter(numero_control=numero_control).first()

    # Metodo para borrar el perfil
    def eliminar_perfil(self):
        """Elimina el perfil actual."""
        self.delete()

