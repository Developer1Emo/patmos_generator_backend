from abc import ABC, abstractmethod

class UserServiceInterface(ABC):
    @abstractmethod
    def crear_usuario(self, identificacion, nombre, rol, email, password, estadoUsuario, telefono, direccion):
        pass

    @abstractmethod
    def obtener_usuario_por_identificacion(self, user_id):
        pass