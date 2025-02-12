from rest_framework.views import APIView
from rest_framework.response import Response
from app_core.services.implementations.usuario_service import UserService
from app_core.services.interfaces.usuario_service_interface import UserServiceInterface
from app_core.serializers.usuario_serializer import UsuarioSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class CreateUsuarioView(APIView):
    usuario_service: UserServiceInterface = UserService()
    @extend_schema(
        responses={200: UsuarioSerializer},
        
    )
    def post(self, request):
        identificacion = request.data.get('identificacion')
        nombre = request.data.get('nombre')
        rol = request.data.get('rol')
        email = request.data.get('email')
        password = request.data.get('password')
        estadoUsuario = True  # Asumimos que el status por defecto es True
        telefono = request.data.get('telefono')
        direccion = request.data.get('direccion')
        
        # Llamamos al servicio para crear el usuario
        try:
            usuario = self.usuario_service.crear_usuario(
                identificacion, nombre, rol, email, password, estadoUsuario, telefono, direccion
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)

        # Serializamos la respuesta y la devolvemos
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=201)
    
class ObtenerUsuarioView(APIView):
    
    print("ObtenerUsuarioView")
    
    
