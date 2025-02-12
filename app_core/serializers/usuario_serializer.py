from rest_framework import serializers
from app_core.models.usuario import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'identificacion', 'nombre', 'rol', 'email', 'password', 'estadoUsuario', 'telefono', 'direccion']
