
from app_core.models.usuario import Usuario
from app_core.services.interfaces.auth_service_interface import AuthServiceInterface
from app_core.utils.jwt_utils import JWTUtils
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password

class AuthService(AuthServiceInterface):
    
    def __init__(self, jwt_utils: JWTUtils):
        # Usar inyección de dependencias
        self.jUtils = jwt_utils

    def iniciarSesion(self,email,password):
        # Buscar el usuario en la base de datos
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            #return "El usuario o la contraseña no son válidos"
            raise Exception("El usuario o la contraseña no son válidos")

         # Verificar la contraseña ingresada
        if not check_password(password, usuario.password):  # Compara el hash
            #return "La contraseña es incorrecta"
            raise Exception("La contraseña es incorrecta")

        # Verificar el estado de la cuenta (si está activa)
        if not usuario.estadoUsuario:
            #return "La cuenta está inactiva"
            raise Exception("La cuenta está inactiva")

        # Generar el token JWT
        token =self.jUtils.generar_token(usuario.id,usuario.rol,usuario.email,usuario.nombre)

        return token