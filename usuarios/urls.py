
from django.urls import path
from . import views

# Definición de las rutas de la aplicación de usuarios
urlpatterns = [
    path('test-db/', views.test_db_connection, name='test_db_connection'),
]

"""
urlpatterns = [

    # Ruta para el registro de usuarios
    path('register/', views.register, name='register'),
    # Ruta para el inicio de sesión
    path('login/', views.login, name='login'),
    # Ruta para el cierre de sesión
    path('logout/', views.logout, name='logout'),
    # Ruta para ver el perfil del usuario
    path('profile/', views.profile, name='profile'),
    # Ruta para actualizar la información del usuario
    path('update/', views.update, name='update'),
    # Ruta para eliminar la cuenta del usuario
    path('delete/', views.delete, name='delete'),
    # Ruta para cambiar la contraseña del usuario
    path('password/', views.password, name='password'),
    # Ruta para solicitar el restablecimiento de la contraseña
    path('password_reset/', views.password_reset, name='password_reset'),
    # Ruta que indica que la solicitud de restablecimiento de contraseña se ha enviado
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    # Ruta para confirmar el restablecimiento de la contraseña
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    # Ruta que indica que el restablecimiento de la contraseña se ha completado
    path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),

]
"""

