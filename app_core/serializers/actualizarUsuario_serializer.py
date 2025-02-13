from rest_framework import serializers

class ActualizarUsuarioSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100)
    identificacion = serializers.CharField(max_length=100)
    nombre = serializers.CharField(max_length=255)
    rol = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    estadoUsuario = serializers.BooleanField()
    telefono = serializers.CharField(max_length=20)
    direccion = serializers.CharField(max_length=255)