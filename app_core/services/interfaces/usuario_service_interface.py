from abc import ABC, abstractmethod

class UserServiceInterface(ABC):
    @abstractmethod
    def crear_usuario(self, identificacion, nombre, rol, email, password, estadoUsuario, telefono, direccion):
        pass

    @abstractmethod
    def obtener_usuario_por_id(self, user_id):
        pass

    @abstractmethod
    def obtenerUsuarios(self):
        pass

    @abstractmethod
    def obtener_usuario_por_identificacion(self, user_identificacion):
        pass
    @abstractmethod
    def actualizarUsuario(self, user_id,data):
        pass