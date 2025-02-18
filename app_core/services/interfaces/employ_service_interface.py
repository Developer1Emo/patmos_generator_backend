
from abc import ABC, abstractmethod

class EmployServiceInterface(ABC):

    @abstractmethod
    def crear_plano(self,id):
        pass
    @abstractmethod
    def obtenerFacturasPendientes(self):
        pass