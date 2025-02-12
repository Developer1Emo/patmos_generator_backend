from django.contrib.auth.hashers import make_password
from app_core.models.usuario import Usuario
from app_core.services.interfaces.usuario_service_interface import UserServiceInterface
from django.db import IntegrityError

class UserService(UserServiceInterface):
    
    def crear_usuario(self, identificacion, nombre, rol, email, password, estadoUsuario, telefono, direccion):
        
        usuario = self.obtener_usuario_por_identificacion(identificacion)
        if usuario:
            raise ValueError("Error al crear el usuario. El identificador ya está en uso.") 
        else:
            usuario = self.obtener_usuario_por_email(email)
            if usuario:
                raise ValueError("Error al crear el usuario. El correo ya está en uso.")
            else:
                try:
                    password_hash = make_password(password)  # Cifra la contraseña
                    usuario = Usuario.objects.create(
                        identificacion=identificacion,
                        nombre=nombre,
                        rol=rol,
                        email=email,
                        password=password_hash,
                        estadoUsuario=True,
                        telefono=telefono,
                        direccion=direccion
                    )
                    # Llamamos al método save() para guardar el usuario en la base de datos
                    usuario.save()
                    return usuario
                except Exception as e:
                    raise Exception("Error al crear el usuario. " + str(e))
              
    
    def obtener_usuario_por_identificacion(self, identificacion):
        try:
            usuario = Usuario.objects.get(identificacion=identificacion, estadoUsuario=True)
            return usuario
        except Usuario.DoesNotExist:
            return None
        
    def obtener_usuario_por_email(self, email):
        try:
            usuario = Usuario.objects.get(email=email)
            return usuario
        except Usuario.DoesNotExist:
            return None
