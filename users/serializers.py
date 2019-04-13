from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    token = serializers.CharField(max_length=255)
