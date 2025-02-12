from rest_framework.views import APIView
from rest_framework.response import Response
from app_core.services.implementations.usuario_service import UserService
from app_core.services.interfaces.usuario_service_interface import UserServiceInterface
from app_core.serializers.usuario_serializer import UsuarioSerializer
from app_core.serializers.crearUsuarioDTO_serializer import CrearUsuarioSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class CreateUsuarioView(APIView):
    usuario_service: UserServiceInterface = UserService()
    @extend_schema(
        responses={200: UsuarioSerializer},
        
    )
    def post(self, request):

        # Usamos el serializer para deserializar los datos
        serializer = CrearUsuarioSerializer(data=request.data)

        
        # Llamamos al servicio para crear el usuario
        try:
            if serializer.is_valid():
                # Llamamos al servicio para crear el usuario
                usuario = self.usuario_service.crear_usuario(
                    serializer.validated_data['identificacion'],
                    serializer.validated_data['nombreCompleto'],
                    serializer.validated_data['rol'],
                    serializer.validated_data['email'],
                    serializer.validated_data['password'],
                    True,
                    serializer.validated_data['telefono'],
                    serializer.validated_data['direccion'])
            else:
                return Response("Error en if"+serializer.errors, status=400)
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)

        # Serializamos la respuesta y la devolvemos
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=201)
    
class ObtenerUsuarioView(APIView):
    
    print("ObtenerUsuarioView")
    
    
