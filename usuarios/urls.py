# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from usuarios.views import RolViewSet, UsuarioViewSet, PerfilViewSet, LoginViewSet, LogoutViewSet

router = DefaultRouter()
router.register(r'roles', RolViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'perfiles', PerfilViewSet)
router.register(r'login', LoginViewSet, basename='login')
router.register(r'logout',LogoutViewSet, basename='logout')

urlpatterns = [
    path('', include(router.urls)),
]
