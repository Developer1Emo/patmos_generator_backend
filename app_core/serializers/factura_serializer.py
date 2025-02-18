from rest_framework import serializers

class FacturaSerializer(serializers.Serializer):
    compania = serializers.CharField(max_length=200)
    co = serializers.CharField(max_length=50)
    tipo_documento = serializers.CharField(max_length=50)
    consecutivo = serializers.CharField(max_length=50)