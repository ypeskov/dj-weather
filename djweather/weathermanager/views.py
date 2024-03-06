from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from icecream import ic

from core.responses.exceptions.exceptions import ApiException
from core.responses.successes.successes import ApiSuccessResponse
from .serializers import CityWeatherSerializer
from .services.service_factory import get_weather_service
from .services.WeatherService import WeatherService


class CurrentWeatherView(APIView):
    def post(self, request):
        serializer = CityWeatherSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            city = serializer.validated_data.get('city')

            service: WeatherService = get_weather_service()
            try:
                response = service.get_weather(city)
                serializer.validated_data['current_weather'] = response.json()
                data, status_code = ApiSuccessResponse(
                    message="Current weather fetched successfully.",
                    details=serializer.data
                ).to_response()
                return Response(data=data, status=status_code)
            except ApiException as e:
                if isinstance(e, ApiException):
                    if e.error_code == 'INVALID_CITY':
                        raise ApiException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            error_code='INVALID_CITY',
                            message="City is invalid. Please provide a valid city."
                        )

                raise ApiException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    error_code='INTERNAL_SERVER_ERROR',
                    message="Error while fetching current weather from tomorrow.io. Please try again later."
                )

