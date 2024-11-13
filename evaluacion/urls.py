
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from evaluacion.views import EvaluacionViewSet

router = DefaultRouter()
router.register(r'evaluaciones', EvaluacionViewSet)
urlpatterns = [
    path('', include(router.urls)),
]