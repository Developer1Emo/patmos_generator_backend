import jwt
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime

class JWTAuthenticationMiddleware:
    """
    Middleware para la validación de JWT en las solicitudes y validación del rol ADMINISTRADOR
    para rutas que comienzan con '/administrator'.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtenemos el token del encabezado Authorization
        token = self.get_token_from_header(request)
        
        if token:
            try:
                # Verificamos y decodificamos el token
                payload = self.decode_jwt_token(token)
                
                # Opcional: Si deseas hacer algo con el payload decodificado,
                # como establecer el usuario autenticado, puedes hacerlo aquí.
                request.user_payload = payload

                # Verificar si la ruta es de administrador y si el rol es ADMINISTRADOR
                if self.is_admin_route(request) and payload['rol'] != 'ADMINISTRADOR':
                    return JsonResponse({"error": True, "respuesta": {"mensaje": "Acceso denegado, se requiere rol de ADMINISTRADOR"}}, status=403)

            except Exception as e:
                return JsonResponse({"error": True, "respuesta": {"mensaje": str(e)}}, status=401)
        
        # Si no hay token y la ruta no es de autenticación, retornamos error
        # Se puede modificar para permitir acceso a rutas de autenticación sin token.
        elif not self.is_auth_route(request):
            return JsonResponse({"error": True, "respuesta": {"mensaje": "Token de autenticación requerido"}}, status=401)

        # Continuamos con la siguiente capa de procesamiento de la solicitud
        response = self.get_response(request)
        return response

    def get_token_from_header(self, request):
        """
        Extrae el token del encabezado Authorization de la solicitud.
        """
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None

    def decode_jwt_token(self, token):
        """
        Decodifica y verifica un token JWT.
        """
        try:
            # Decodificamos el token usando la clave secreta de configuración
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            
            # Comprobamos que el token no haya expirado
            expiration_time = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)  # Crear un datetime consciente de la zona horaria UTC
            current_time = datetime.now(tz=timezone.utc)  # Obtener la hora actual en UTC y consciente de la zona horaria

            if expiration_time < current_time:
                raise AuthenticationFailed("El token ha expirado")
            
            return payload
        
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("El token ha expirado")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Token inválido")
        except Exception as e:
            raise AuthenticationFailed(f"Error al procesar el token: {str(e)}")

    def is_auth_route(self, request):
        """
        Determina si la solicitud es una ruta de autenticación (no requiere token).
        """
        # Puedes agregar aquí las rutas que no requieren autenticación, como la de login.
        auth_routes = ['/auth/iniciar-sesion', '/auth/crearUsuarios']
        return any(request.path.startswith(route) for route in auth_routes)

    def is_admin_route(self, request):
        """
        Determina si la ruta solicitada es una ruta de administrador (comienza con /administrator).
        """
        return request.path.startswith('/administrator')
