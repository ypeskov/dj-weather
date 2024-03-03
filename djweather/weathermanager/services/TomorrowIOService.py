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

    def fetch_weather(self, uri, params=None, headers=None):
        if not headers:
            headers = {"accept": "application/json"}

        url = f"{BASE_URL}{uri}&apikey={self.api_key}"
        response = requests.get(url, headers=headers)
        if response.status_code == status.HTTP_200_OK:
            return response
        else:
            raise ApiException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code='INTERNAL_SERVER_ERROR',
                message="Error while fetching weather from tomorrow.io. Please try again later.",
                details=response.json()
            )

    def get_current_weather(self, city):
        uri = f"{endpoints.REALTIME_WEATHER}?location={city}"
        return self.fetch_weather(uri)

