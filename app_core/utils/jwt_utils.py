import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

class JWTUtils:
    
    @staticmethod
    def generar_token(id,rol,email,nombre):
        """
        Genera un JWT con un email y un conjunto de claims.
        """
        payload = {
            'id': id,
            'rol': 'ADMINISTRADOR' if rol == 'ADMINISTRADOR' else 'EMPLEADO',
            'email':email,
            'nombre': nombre,
            'exp': timezone.now() + timedelta(hours=1),  # Expiración del token en 1 hora
            'iat': timezone.now(),  # Fecha de emisión
        }
        
        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def parse_jwt(jwt_string):
        """
        Parse y verifica un JWT.
        """
        try:
            payload = jwt.decode(jwt_string, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            return payload
        except ExpiredSignatureError:
            raise Exception("El token ha expirado")
        except InvalidTokenError:
            raise Exception("El token no es válido")
        except Exception as e:
            raise Exception(str(e))
