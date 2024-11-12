from django.urls import path
from .views import ActividadDeleteView

urlpatterns = [
    path('actividades/<uuid:guid>/', ActividadDeleteView.as_view(), name='actividad-delete'),
]
