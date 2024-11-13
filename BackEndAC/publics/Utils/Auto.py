from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication


class RolePermission(BasePermission):
    required_roles = []  # Define los roles permitidos para la ruta específica

    def has_permission(self, request, view):
        # Usamos JWTAuthentication para obtener el usuario y el token
        jwt_authenticator = JWTAuthentication()
        try:
            # Autenticar el token y obtener el usuario
            user, token = jwt_authenticator.authenticate(request)

            # Obtener el rol desde el token
            user_role = token.get('rol')  # Asegúrate de que 'rol' es el nombre correcto

            # Verificar si el rol del usuario está en los roles permitidos
            if user_role in self.required_roles:
                return True
            else:
                raise PermissionDenied("No tienes permiso para acceder a esta ruta.")

        except Exception as e:
            # Manejar excepciones relacionadas con la autenticación
            raise PermissionDenied(f"Autenticación fallida: {str(e)}")