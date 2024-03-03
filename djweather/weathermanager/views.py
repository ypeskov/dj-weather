import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from icecream import ic

from core.responses.exceptions.exceptions import ApiException
from core.responses.successes.successes import ApiSuccessResponse
from .serializers import CityWeatherSerializer

API_KEY = getattr(settings, 'TOMORROW_IO_API_KEY', '1111111111')


class CurrentWeatherView(APIView):
    def post(self, request):
        serializer = CityWeatherSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            city = serializer.validated_data.get('city')
            url = f"https://api.tomorrow.io/v4/weather/realtime?location={city}&apikey={API_KEY}"
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)
            if response.status_code == status.HTTP_200_OK:
                serializer.validated_data['current_weather'] = response.json()
                data, status_code = ApiSuccessResponse(
                    message="Current weather fetched successfully.",
                    details=serializer.data
                ).to_response()

                return Response(data=data, status=status_code)
            else:
                raise ApiException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    error_code='INTERNAL_SERVER_ERROR',
                    message="Error while fetching current weather from tomorrow.io. Please try again later."
                )

