# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from usuarios.views import RolViewSet, UsuarioViewSet, PerfilViewSet, LoginViewSet

router = DefaultRouter()
router.register(r'roles', RolViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'perfiles', PerfilViewSet)
router.register(r'login', LoginViewSet, basename='login')  # Registro del LoginViewSet

urlpatterns = [
    path('', include(router.urls)),
]
