from abc import ABC, abstractmethod

class RegistroServiceInterface(ABC):

    @abstractmethod
    def crear_registro(self, user, ruta_archivo_log):
        pass