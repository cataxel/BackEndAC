from uuid import uuid4

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
    rol = serializers.UUIDField()

    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'contraseña', 'rol']
        extra_kwargs = {
            'contraseña':  {'write_only': True, 'required': True}
        }

    def create(self, validated_data):
        """
        Crea una nueva instancia de Usuario.
        """
        rol_guid= validated_data.pop('rol')
        rol = Roles.objects.get(guid=rol_guid)
        contrasena = validated_data.get('contraseña')
        usuario = Usuario(**validated_data, rol=rol)
        usuario.set_password(contrasena)
        usuario.guid = uuid4()
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        """
        Actualiza una instancia existente de Usuario.
        """
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.correo = validated_data.get('correo', instance.correo)

        if 'contraseña' in validated_data:
            contraseña = validated_data.pop('contraseña')
            instance.set_password(contraseña)

        if 'rol' in validated_data:
            rol_guid = validated_data.pop('rol')
            instance.rol = Roles.objects.get(guid=rol_guid)

        instance.save()
        return instance