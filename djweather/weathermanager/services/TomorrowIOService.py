import requests

from rest_framework import status
from django.conf import settings

from icecream import ic

from core.responses.exceptions.exceptions import ApiException
from .WeatherService import WeatherService
from .TomorrowIOEndpoints import TomorrowIOEndpoints

API_KEY = getattr(settings, 'TOMORROW_IO_API_KEY', '1111111111')
BASE_URL = "https://api.tomorrow.io/v4"
endpoints = TomorrowIOEndpoints()


class TomorrowIOService(WeatherService):
    def __init__(self):
        super().__init__()
        self.api_key = API_KEY

    def _fetch_weather(self, uri, params=None, headers=None):
        if not headers:
            headers = {"accept": "application/json"}

        url = f"{BASE_URL}{uri}&apikey={self.api_key}"
        response = requests.get(url, headers=headers)
        # ic(response.json())
        # ic(response.status_code)
        if response.status_code == status.HTTP_200_OK:
            return response
        elif response.status_code == status.HTTP_400_BAD_REQUEST and response.json().get('code') == 400001:
            raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code='INVALID_CITY',
                message="City is invalid. Please provide a valid city.",
                details=response.json()
            )
        else:
            raise ApiException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code='INTERNAL_SERVER_ERROR',
                message="Error while fetching weather from tomorrow.io. Please try again later.",
                details=response.json()
            )

    def get_weather(self, city: str = None, weather_type: str = "current", **kwargs):
        if city is None:
            raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code='INVALID_INPUT',
                message="City is required to fetch weather."
            )
        if weather_type == "current":
            return self._get_current_weather(city)
        else:
            return self._get_forecast_weather(city)

    def _get_current_weather(self, city):
        uri = f"{endpoints.REALTIME_WEATHER}?location={city}"
        return self._fetch_weather(uri)

    def _get_forecast_weather(self, city):
        uri = f"{endpoints.FORECAST_WEATHER}?location={city}"
        return self._fetch_weather(uri)

