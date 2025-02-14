from abc import ABC, abstractmethod

class AuthServiceInterface(ABC):
    @abstractmethod
    def __init__(self, jwt_utils):  # Recibe JWTUtils como parámetro
        self.jwt_utils = jwt_utils
        
    @abstractmethod
    def iniciarSesion(self,email,password):
        pass