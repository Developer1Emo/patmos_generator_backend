from rest_framework import serializers
class MensajeSerializer(serializers.Serializer):
    error = serializers.BooleanField()
    respuesta = serializers.JSONField()