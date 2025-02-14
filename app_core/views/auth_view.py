from rest_framework.views import APIView
from rest_framework.response import Response
from app_core.serializers.login_Serializer import LoginSerializer
from app_core.serializers.token_Serializer import TokenSerializer
from app_core.services.implementations.auth_service import AuthService
from app_core.services.interfaces.auth_service_interface import AuthServiceInterface
from app_core.utils.jwt_utils import JWTUtils
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.pagination import PageNumberPagination  # Importa la paginación
from rest_framework.exceptions import NotFound
from rest_framework import status

class IniciarSesionView(APIView):
    jwt_utils = JWTUtils()
    auth_service: AuthServiceInterface = AuthService(jwt_utils)
    
    def post(self, request):
        # Validar el serializer de login
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Obtener los datos del formulario
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                token = self.auth_service.iniciarSesion(email, password)
                
                # Crear el serializer para la respuesta con el token
                token_serializer = TokenSerializer(data={'token': token})
                
                if token_serializer.is_valid():
                    error=False
                    print(token_serializer)
                    return Response({'error': error, 'respuesta': token_serializer.data}, status=200)
                error=True  
                respuesta= {"mensaje":""+token_serializer.errors}

                return Response({'error': error, 'respuesta': respuesta}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # En caso de error, devolver un mensaje de error
                error=True 
                respuesta= {"mensaje":""+str(e)}
                return Response({'error': error, 'respuesta': respuesta}, status=status.HTTP_400_BAD_REQUEST)   
        else:
            # Si el serializer de login no es válido
            error=True  
            respuesta= {"mensaje":""+serializer.errors}
            return Response({'error': error, 'respuesta': respuesta}, status=status.HTTP_400_BAD_REQUEST)