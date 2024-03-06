from abc import abstractmethod
from enum import Enum


class WeatherType(Enum):
    CURRENT = "current"
    FORECAST = "forecast"


class WeatherService:
    def __init__(self):
        self.api_key = "1111111111"

    @abstractmethod
    def get_weather(self, city: str = None, weather_type: str = WeatherType.CURRENT.value, **kwargs):
        pass

    @abstractmethod
    def _get_current_weather(self, city):
        pass

    @abstractmethod
    def _get_forecast_weather(self, city):
        pass
