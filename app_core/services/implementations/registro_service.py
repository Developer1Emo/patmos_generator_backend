from app_core.models.registro import Registro
from app_core.services.interfaces.registro_service_interface import RegistroServiceInterface

class RegistroService(RegistroServiceInterface):
    def crear_registro(self, user, ruta_archivo_log):
        # Aquí puedes agregar validaciones adicionales si es necesario
        registro = Registro.objects.create(idUser=user, rutaArchivoLog=ruta_archivo_log)
        return registro
