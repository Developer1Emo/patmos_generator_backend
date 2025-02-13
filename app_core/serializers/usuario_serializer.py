from rest_framework import serializers
from app_core.models.usuario import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'identificacion', 'nombre', 'rol', 'email', 'password', 'estadoUsuario', 'telefono', 'direccion']
    def update(self, instance, validated_data):
        # Si se envió un nuevo password, lo actualizamos
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        # Actualizamos los campos restantes
        for attr, value in validated_data.items():
            if attr != 'password':  # Excluimos 'password' para evitar cambiarlo sin querer
                setattr(instance, attr, value)
        
        # Guardamos la instancia actualizada
        instance.save()
        return instance
