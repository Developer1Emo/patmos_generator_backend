from rest_framework import serializers

class CrearUsuarioSerializer(serializers.Serializer):
    identificacion = serializers.CharField(max_length=100)
    nombreCompleto = serializers.CharField(max_length=255)
    rol = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, max_length=100)
    telefono = serializers.CharField(max_length=20)
    direccion = serializers.CharField(max_length=255)
