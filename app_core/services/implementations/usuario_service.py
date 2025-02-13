from django.contrib.auth.hashers import make_password
from app_core.models.usuario import Usuario

from app_core.serializers.usuario_serializer import UsuarioSerializer
from app_core.services.interfaces.usuario_service_interface import UserServiceInterface
from django.db import IntegrityError

class UserService(UserServiceInterface):
    
    def crear_usuario(self, identificacion, nombre, rol, email, password, estadoUsuario, telefono, direccion):
        
        usuario = self.obtener_usuario_por_identificacion(identificacion)
        if usuario:
            return "Error al crear el usuario. El identificador ya está en uso."
            
        else:
            usuario = self.obtener_usuario_por_email(email)
            if usuario:
                return "Error al crear el usuario. El correo ya está en uso."
                
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
                    return "Exito"
                except Exception as e:
                    return "Error al crear el usuario. " + str(e)
              
    def obtener_usuario_por_id(self, id):
        try:
            usuario = Usuario.objects.get(id=id)
            
            return usuario
        except Usuario.DoesNotExist:
            return None

    def obtener_usuario_por_identificacion(self, user_identificacion):
        try:
            usuario = Usuario.objects.get(identificacion=user_identificacion, estadoUsuario=True)
            return usuario
        except Usuario.DoesNotExist:
            return None
        
    def obtener_usuario_por_email(self, email):
        try:
            usuario = Usuario.objects.get(email=email)
            return usuario
        except Usuario.DoesNotExist:
            return None

    def obtenerUsuarios(self):
        usuarios = Usuario.objects.all()
        return usuarios
    
    def actualizarUsuario(self,idUser,dat):
        try:
            # Intentamos obtener el usuario con el ID proporcionado
            usuario = Usuario.objects.get(id=idUser)
        except Usuario.DoesNotExist:
            return "El usuario que intentas actualizar no existe. Contacta al administrador."
        
        serializer = UsuarioSerializer(usuario, data=dat, partial=True)
        #print(serializer.initial_data)
        # Verificamos si los datos enviados son válidos según las reglas del serializer
        if serializer.is_valid():
            serializer.save()
            
            return "Exito"
        print("Errores de validación:", serializer.errors)
        return "Ha ocurrido un error al intentar actualizar el usuario. Contacta al administrador."