from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Actividad
from .serializers import ActividadSerializer


class ActividadDeleteView(generics.DestroyAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
    lookup_field = 'guid'

class ActividadCreateView(generics.CreateAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer

class ActividadUpdateView(generics.UpdateAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
    lookup_field = 'guid'

class ActividadDetailView(generics.RetrieveAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
    lookup_field = 'guid'