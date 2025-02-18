from django.db import models
from app_core.models.usuario import Usuario

class Registro(models.Model):
    idUser = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='registros')
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha de creación, auto generada
    rutaArchivoLog = models.CharField(max_length=255)

    def __str__(self):
        return f'Registro de {self.idUser.nombre} - {self.fecha}'
