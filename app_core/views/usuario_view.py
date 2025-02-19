import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

from app_core.models.registro import Registro
from app_core.serializers.registro_serializer import RegistroSerializer
from app_core.services.implementations.auth_service import AuthService
from app_core.services.interfaces.auth_service_interface import AuthServiceInterface
from app_core.utils import jwt_utils
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.pagination import PageNumberPagination  # Importa la paginación
from rest_framework.exceptions import NotFound
from rest_framework import status
from app_core.models.usuario import Usuario
from app_core.serializers.actualizarUsuario_serializer import ActualizarUsuarioSerializer
from app_core.services.implementations.usuario_service import UserService
from app_core.services.interfaces.usuario_service_interface import UserServiceInterface
from app_core.serializers.usuario_serializer import UsuarioSerializer
from app_core.serializers.crearUsuarioDTO_serializer import CrearUsuarioSerializer
from app_core.DTO.mensajeDTO import MensajeDTO
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

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
    
class GetUsuariosView(APIView):
    usuario_service: UserServiceInterface = UserService()
    permission_classes:[IsAuthenticated]

    def get(self, request):
        try:
            # Usamos el paginador de Django REST Framework
            paginator = PageNumberPagination()
            paginator.page_size = 10  # Número de usuarios por página
            
            usuarios = self.usuario_service.obtenerUsuarios()

            # Paginamos los usuarios
            result_page = paginator.paginate_queryset(usuarios, request)
            serializer = UsuarioSerializer(result_page, many=True)

            # Devolvemos la paginación junto con los datos serializados
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'error': True,
                'respuesta': {'mensaje': f'Error al obtener los usuarios: {str(e)}'}
            }, status=500)

class GetUsuarioIdView(APIView):
    usuario_service: UserServiceInterface = UserService()

    @extend_schema(
        responses={200: UsuarioSerializer},
    )
    def get(self, request, id, *args, **kwargs):
        try:
            # Intenta obtener el usuario con el ID proporcionado
            usuario = self.usuario_service.obtener_usuario_por_id(id)
            serializer = ActualizarUsuarioSerializer(usuario)
        except Usuario.DoesNotExist:
            raise NotFound("Usuario no encontrado")  # Lanza un error 404 si no existe el usuario

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ActualizarUsuarioView(APIView):
    usuario_service: UserServiceInterface = UserService()
    def put(self, request, id):
        result=self.usuario_service.actualizarUsuario(id,request.data)

        if result == "Exito":
            error=False
            respuesta = {"mensaje": ""+result}
            return Response({'error': error, 'respuesta': respuesta}, status=200)
        else:
            error=True
            respuesta = {"mensaje": ""+result}
            return Response({'error': error, 'respuesta': respuesta}, status=400) 

class GetUsuariosCadenaView(APIView):
    def get(self, request):
        try:
            # Usamos el paginador de Django REST Framework
            paginator = PageNumberPagination()
            paginator.page_size = 10  # Número de usuarios por página
            
            # Obtener la cadena de búsqueda de los parámetros de la query
            busqueda = request.query_params.get('busqueda', '')

            # Filtrar los usuarios si hay una búsqueda
            if busqueda:
                usuarios = Usuario.objects.filter(
                    Q(identificacion__icontains=busqueda) |
                    Q(nombre__icontains=busqueda)
                )
            else:
                # Si no hay búsqueda, obtener todos los usuarios
                usuarios = Usuario.objects.all()

            # Paginamos los usuarios
            result_page = paginator.paginate_queryset(usuarios, request)
            serializer = UsuarioSerializer(result_page, many=True)

            # Devolvemos la paginación junto con los datos serializados
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'error': True,
                'respuesta': {'mensaje': f'Error al obtener los usuarios: {str(e)}'}
            }, status=500)

class GetSearchRegView(APIView):
   def get(self, request):
        try:
            # Usamos el paginador de Django REST Framework
            paginator = PageNumberPagination()
            paginator.page_size = 10  # Número de registros por página

            # Obtener los parámetros de fecha y correo desde la query string
            fecha_desde = request.query_params.get('fecha_desde', '')
            fecha_hasta = request.query_params.get('fecha_hasta', '')
            correo_usuario = request.query_params.get('correo', '')

            # Validación de fechas (si se pasan, deben ser convertibles a datetime)
            if fecha_desde and fecha_hasta:
                try:
                    fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
                    fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d')
                except ValueError:
                    return Response({
                        'error': True,
                        'respuesta': {'mensaje': 'Formato de fecha incorrecto. Use YYYY-MM-DD.'}
                    }, status=400)
            else:
                fecha_desde = fecha_hasta = None

            # Filtrar registros según las condiciones
            if correo_usuario:
                # Si se pasó correo, filtrar por rango de fechas y correo del usuario
                registros = Registro.objects.filter(
                    Q(fecha__gte=fecha_desde) if fecha_desde else Q() &
                    Q(fecha__lte=fecha_hasta) if fecha_hasta else Q() &
                    Q(usuario__email__icontains=correo_usuario)
                )
            else:
                # Si no se pasó correo, solo filtrar por el rango de fechas
                registros = Registro.objects.filter(
                    Q(fecha__gte=fecha_desde) if fecha_desde else Q() &
                    Q(fecha__lte=fecha_hasta) if fecha_hasta else Q()
                )

            # Paginamos los registros
            result_page = paginator.paginate_queryset(registros, request)
            serializer = RegistroSerializer(result_page, many=True)

            # Devolvemos la paginación junto con los datos serializados
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'error': True,
                'respuesta': {'mensaje': f'Error al obtener los registros: {str(e)}'}
            }, status=500)