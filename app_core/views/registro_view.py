from rest_framework.views import APIView
from rest_framework.response import Response
from app_core.services.implementations.registro_service import RegistroService
from app_core.services.interfaces.registro_service_interface import RegistroServiceInterface
from app_core.serializers.registro_serializer import RegistroSerializer
from app_core.models.usuario import Usuario

class RegistroView(APIView):
    # Usamos la interfaz para poder usar cualquier implementación
    registro_service: RegistroServiceInterface = RegistroService()

    def post(self, request):
        # Primero obtenemos el usuario desde la base de datos
        try:
            usuario = Usuario.objects.get(id=request.data['idUser'])
        except Usuario.DoesNotExist:
            return Response({"detail": "Usuario no encontrado."}, status=404)

        # Usamos el servicio para crear el registro
        registro = self.registro_service.crear_registro(usuario, request.data['rutaArchivoLog'])

        # Serializamos el objeto de registro para devolverlo como respuesta
        serializer = RegistroSerializer(registro)
        return Response(serializer.data, status=201)
