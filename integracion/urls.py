
from django.urls import path
from integracion.views import CloudinaryImageView

urlpatterns = [
    path('cloudinary-images/', CloudinaryImageView.as_view(), name='cloudinary-images'),
]