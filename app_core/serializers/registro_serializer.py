from rest_framework import serializers
from app_core.models.registro import Registro

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = ['id', 'idUser', 'fecha', 'rutaArchivoLog']