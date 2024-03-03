from rest_framework import serializers

from core.responses.exceptions.exceptions import ApiException


class CityWeatherSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100, required=True)
    current_weather = serializers.JSONField(read_only=True)

    def validate(self, attrs):
        if not attrs.get('city'):
            raise ApiException(
                status_code=400,
                error_code='VALIDATION_ERROR',
                message="City is required."
            )
        return attrs
