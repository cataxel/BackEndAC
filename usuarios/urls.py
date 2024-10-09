from django.urls import path, include
from rest_framework.routers import DefaultRouter
from usuarios.views import RolViewSet, UsuarioViewSet

router = DefaultRouter()
router.register(r'roles', RolViewSet)
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]