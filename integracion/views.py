import cloudinary
import cloudinary.api
from cloudinary import uploader
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework import status

from BackEndAC.publics.Generics.Respuesta import APIRespuesta
from integracion.models import CloudinaryImage
from integracion.serializers import CloudinaryImageSerializer


class CloudinaryImageView(APIView):
    parser_class = [MultiPartParser]
    def get(self, request, *args, **kwargs):
        try:
            # Fetch resources from Cloudinary
            cloudinary_response = cloudinary.api.resources(type="upload", resource_type="image",prefix="LoginImages")

            # Parse response to match the schema of CloudinaryImage
            images = [
                CloudinaryImage(
                    public_id=res['public_id'],
                    url=res['secure_url'],
                    created_at=res['created_at'],
                    description=res.get('context', {}).get('custom', {}).get('description', '')
                )
                for res in cloudinary_response['resources']
            ]

            # Serialize the cloudinary images
            serializer = CloudinaryImageSerializer(images, many=True)
            response = APIRespuesta(
                estado=True,
                mensaje="Imagenes",
                data=serializer.data
            )
            return response.to_response()
        except Exception as e:
            cloudinary.logger.error("Error while fetching images from Cloudinary: %s", str(e))
            return APIRespuesta(
                estado=False,
                mensaje="Error al obtener las imágenes",
                data=str(e),
                codigoestado=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).to_response()

    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES.get('file')
            if not file:
                return APIRespuesta(
                    estado = False,
                    mensaje= "error: No se proporciono un archivo.",
                    data=""
                ).to_response()

            upload_result = cloudinary.uploader.upload(file,folder='Profile')
            return APIRespuesta(
                estado=True,
                mensaje="imagen: " + file.name,
                data=upload_result
            ).to_response()
        except Exception as e:
            cloudinary.logger.error("Error while fetching images from Cloudinary: %s", str(e))
            return APIRespuesta(
                estado=False,
                mensaje="Error al subir imagenes",
                data=str(e)
            ).to_response()