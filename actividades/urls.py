from django.urls import path
from .views import ActividadCreateView, ActividadDeleteView, ActividadUpdateView, ActividadDetailView

urlpatterns = [
    path('', ActividadCreateView.as_view(), name='actividad-create'),
    path('delete/<uuid:guid>/', ActividadDeleteView.as_view(), name='actividad-delete'),
    path('update/<uuid:guid>/', ActividadUpdateView.as_view(), name='actividad-update'),
    path('detalle/<uuid:guid>/', ActividadDetailView.as_view(), name='actividad-detail'),

]
