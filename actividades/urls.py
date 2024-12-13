from django.urls import path, include
from rest_framework.routers import DefaultRouter

from actividades.views import ActividadViewSet, GrupoViewSet, InscripcionViewSet, ParticipacionViewSet, \
    AsistenciaViewSet

router = DefaultRouter()
router.register(r'actividades', ActividadViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'inscripciones', InscripcionViewSet)
router.register(r'participaciones', ParticipacionViewSet)

router.register(r'asistencias',AsistenciaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('inscripciones/aprobar/', InscripcionViewSet.as_view({'post': 'aprobar_inscripcion'}), name='aprobar-inscripcion'),
]
