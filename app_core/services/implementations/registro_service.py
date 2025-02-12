from app_core.models.registro import Registro

class RegistroService:
    def crear_registro(self, user, ruta_archivo_log):
        # Aquí puedes agregar validaciones adicionales si es necesario
        registro = Registro.objects.create(idUser=user, rutaArchivoLog=ruta_archivo_log)
        return registro
