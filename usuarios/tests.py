from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from usuarios.models import Usuario


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        """Crea datos reutilizables para las pruebas."""
        self.url = reverse('usuario-list')  # Nombre de la ruta en urls.py (usualmente ViewSet usa -list para create)
        self.valid_data = {
            "username": "testuser",
            "password": "securepassword123",
            "email": "test@example.com",
            "rol":"b290d2cf-48a8-4fd0-91ef-d6fccf450df8"
        }
        self.invalid_data = {
            "username": "",
            "password": "short",
            "email": "not-an-email",
            "rol":"no rol"
        }

    def test_create_usuario_success(self):
        """Prueba de creación exitosa de un usuario."""
        response = self.client.post(self.url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["estado"], True)
        self.assertEqual(response.data["mensaje"], "Usuario creado exitosamente.")
        self.assertIn("data", response.data)

        # Verificar que el usuario fue creado en la base de datos
        self.assertTrue(Usuario.objects.filter(username="testuser").exists())

    def test_create_usuario_invalid_data(self):
        """Prueba de creación fallida con datos inválidos."""
        response = self.client.post(self.url, self.invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["estado"], False)
        self.assertEqual(response.data["mensaje"], "Error al crear el usuario.")
        self.assertIn("data", response.data)