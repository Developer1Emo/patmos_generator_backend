from rest_framework import serializers

class ActualizarUsuarioDTO(serializers.Serializer):
    id = serializers.IntegerField()
    identificacion = serializers.CharField(max_length=50)
    nombre = serializers.CharField(max_length=100)
    rol = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    estadoUsuario = serializers.BooleanField()
    telefono = serializers.CharField(max_length=15)
    direccion = serializers.CharField(max_length=255)

    # Si necesitas agregar validaciones personalizadas, puedes hacerlo aquí
    def validate_identificacion(self, value):
        # Ejemplo de validación: asegurar que la identificación no esté vacía
        if not value:
            raise serializers.ValidationError("La identificación es obligatoria.")
        return value
