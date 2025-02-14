from rest_framework import serializers

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, allow_blank=False)
