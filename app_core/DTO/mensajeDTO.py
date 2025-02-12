from rest_framework import serializers

class MensajeDTO(serializers.Serializer):
    error = serializers.BooleanField()
    respuesta = serializers.JSONField()