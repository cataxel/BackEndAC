from django.urls import path, include
from rest_framework.routers import DefaultRouter

from actividades.views import ActividadViewSet, GrupoViewSet, InscripcionViewSet

router = DefaultRouter()
router.register(r'actividades', ActividadViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'inscripciones', InscripcionViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
