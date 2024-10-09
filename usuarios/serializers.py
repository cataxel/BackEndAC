from rest_framework import serializers
from .models import Usuario, Roles

class RolesSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Roles.
    """

    class Meta:
        model = Roles
        fields = ['nombre']


def validate_correo(value):
    """
    Valida que el correo no esté en uso.

    Args:
        value (str): El correo a validar.

    Raises:
        serializers.ValidationError: Si el correo ya está en uso.

    Returns:
        str: El correo validado.
    """
    if Usuario.objects.filter(correo=value).exists():
        raise serializers.ValidationError('El correo ya está en uso')
    return value


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Usuario.
    """
    rol = serializers.SlugRelatedField(
        queryset=Roles.objects.all(),
        slug_field='nombre'
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'contraseña', 'rol']

    def create(self, validated_data):
        """
        Crea una nueva instancia de Usuario.

        Args:
            validated_data (dict): Los datos validados para crear el usuario.

        Raises:
            serializers.ValidationError: Si el correo ya está en uso.

        Returns:
            Usuario: La instancia de Usuario creada.
        """
        rol_data = validated_data.pop('rol')
        rol = Roles.objects.get(nombre=rol_data)
        if Usuario.objects.filter(correo=validated_data.get('correo')).exists():
            raise serializers.ValidationError('El correo ya está en uso')
        usuario = Usuario.objects.create(rol=rol, **validated_data)
        return usuario

    def update(self, instance, validated_data):
        """
        Actualiza una instancia existente de Usuario.

        Args:
            instance (Usuario): La instancia de Usuario a actualizar.
            validated_data (dict): Los datos validados para actualizar el usuario.

        Returns:
            Usuario: La instancia de Usuario actualizada.
        """
        rol_data = validated_data.pop('rol')
        rol = Roles.objects.get_or_create(**rol_data)[0]
        instance.rol = rol
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.correo = validated_data.get('correo', instance.correo)
        instance.contraseña = validated_data.get('contraseña', instance.contraseña)
        instance.save()
        return instance