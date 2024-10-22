from typing import Optional, Any

from rest_framework.response import Response
from rest_framework import status


class APIRespuesta:
    def __init__(self,
                 estado:bool,
                 mensaje:str,
                 data: Optional[Any] = None,
                 codigoestado:int = status.HTTP_200_OK):
        """
        Clase personalizada para estructurar las respuestas de la API.

        :param estado: Indica si la operación fue exitosa.
        :param mensaje: Mensaje explicativo sobre la operación.
        :param data: Datos adicionales que se devuelven (opcional).
        :param codigoEstado: Código de estado HTTP (default: 200).
        """
        self.mensaje = mensaje
        self.estado = estado
        self.codigoEstado = codigoestado
        self.data = data

    def to_response(self) -> Response:
        """Convierte la respuesta en un objeto `Response` de DRF."""
        content = {
            "estado": self.estado,
            "mensaje": self.mensaje,
            "data": self.data,
        }
        return Response(content, status=self.codigoEstado)

