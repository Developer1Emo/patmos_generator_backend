from django.db import models

class Usuario(models.Model):
    identificacion = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=50,choices=[('ADMINISTRADOR', 'Administrador'), ('EMPLEADO', 'Empleado')])
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    estadoUsuario = models.BooleanField(default=True)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
