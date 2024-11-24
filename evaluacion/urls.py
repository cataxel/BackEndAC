
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from evaluacion.views import EvaluacionViewSet, ListaEsperaViewSet

router = DefaultRouter()
router.register(r'evaluaciones', EvaluacionViewSet)
router.register(r'ListaEspera', ListaEsperaViewSet)
urlpatterns = [
    path('', include(router.urls)),
]