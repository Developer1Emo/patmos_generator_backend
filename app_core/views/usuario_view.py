from rest_framework.views import APIView
from rest_framework.response import Response
from app_core.services.implementations.usuario_service import UserService
from app_core.services.interfaces.usuario_service_interface import UserServiceInterface
from app_core.serializers.usuario_serializer import UsuarioSerializer
from app_core.serializers.crearUsuarioDTO_serializer import CrearUsuarioSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from app_core.DTO.mensajeDTO import MensajeDTO


class CreateUsuarioView(APIView):
    usuario_service: UserServiceInterface = UserService()
    @extend_schema(
        responses={200: UsuarioSerializer},
        
    )
    def post(self, request):
        # Usamos el serializer para deserializar los datos
        serializer = CrearUsuarioSerializer(data=request.data)

        # Validamos el serializer antes de acceder a sus datos
        if serializer.is_valid():
            try:
                # Llamamos al servicio para crear el usuario
                usuario = self.usuario_service.crear_usuario(
                    serializer.validated_data['identificacion'],
                    serializer.validated_data['nombreCompleto'],
                    serializer.validated_data['rol'],
                    serializer.validated_data['email'],
                    serializer.validated_data['password'],
                    True,  # Estado del usuario
                    serializer.validated_data['telefono'],
                    serializer.validated_data['direccion']
                )
                if usuario == "Exito":
                    # Si la creación del usuario es exitosa
                    error = False
                    respuesta = {"mensaje": "Operación exitosa"}
                    # Aquí solo pasamos el diccionario directamente
                    return Response({'error': error, 'respuesta': respuesta}, status=201)
                else:
                    # Si la creación del usuario es exitosa
                    error = True
                    respuesta = {"mensaje": ""+usuario}
                    # Aquí solo pasamos el diccionario directamente
                    return Response({'error': error, 'respuesta': respuesta}, status=400)
            except ValueError as e:
                # Si ocurre un error en la creación del usuario
                error = True
                respuesta = {"mensaje": str(e)}
                # Aquí solo pasamos el diccionario directamente
                return Response({'error': error, 'respuesta': respuesta}, status=400)
        else:
            # Si el serializer no es válido
            error = True
            respuesta = {"mensaje": "Ha ocurrido algo al tratar de Guardar el usuario. Contacte al administrador"}
            # Aquí solo pasamos el diccionario directamente
            return Response({'error': error, 'respuesta': respuesta}, status=400)
    
class ObtenerUsuarioView(APIView):
    
    print("ObtenerUsuarioView")
    
    
