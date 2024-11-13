from uuid import uuid4

from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Usuario, Roles, Perfil


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
        fields = ['guid','nombre', 'correo', 'contraseña', 'rol']
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

    def delete(self, instance):
        """
        Elimina una instancia existente de Usuario.
        """
        instance.delete()
        return {"mensaje": "Usuario eliminado exitosamente"}


class PerfilSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Perfiles.
    """
    usuario = serializers.UUIDField()

    class Meta:
        model = Perfil
        fields = ['usuario','telefono','direccion','carrera','numero_control']

    def create(self, validated_data):
        usuario_guid = validated_data.pop('usuario')
        # Buscamos el usuario asociado
        try:
            usuario = Usuario.objects.get(guid=usuario_guid)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Usuario no encontrado.")

        # Verificar si el usuario ya tiene un perfil
        if Perfil.objects.filter(usuario=usuario).exists():
            raise serializers.ValidationError("El usuario ya tiene un perfil asociado.")
        perfil = Perfil(**validated_data, usuario=usuario)
        perfil.guid = uuid4()
        perfil.save()
        return perfil

    def update(self, instance, validated_data):
        usuario_guid = validated_data.pop('usuario', None)

        # Verificar si se proporciona un nuevo usuario y actualizarlo
        if usuario_guid and instance.usuario.guid != usuario_guid:
            try:
                usuario = Usuario.objects.get(guid=usuario_guid)

                # Verificar que el nuevo usuario no tenga ya un perfil
                if Perfil.objects.filter(usuario=usuario).exists():
                    raise serializers.ValidationError("El nuevo usuario ya tiene un perfil asociado.")

                instance.usuario = usuario
            except Usuario.DoesNotExist:
                raise serializers.ValidationError("Usuario no encontrado.")

        # Actualizar el teléfono utilizando el metodo del modelo
        nuevo_telefono = validated_data.get('telefono')
        if nuevo_telefono:
            instance.actualizar_telefono(nuevo_telefono)

        # Actualizar la dirección si se proporciona
        instance.direccion = validated_data.get('direccion', instance.direccion)

        # Actualizar la carrera y validar si está asignada
        nueva_carrera = validated_data.get('carrera')
        if nueva_carrera:
            instance.carrera = nueva_carrera
            if not instance.tiene_carrera():
                raise serializers.ValidationError("Debe asignarse una carrera válida.")

        # Actualizar el número de control si se proporciona
        numero_control = validated_data.get('numero_control')
        if numero_control:
            instance.numero_control = numero_control

        # Guardar la instancia actualizada
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return {"mensaje": "datos de perfil eliminado exitosamente"}


