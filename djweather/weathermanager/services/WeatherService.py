from abc import abstractmethod


class WeatherService:
    def __init__(self):
        self.api_key = "1111111111"

    @abstractmethod
    def get_weather(self, city: str = None, weather_type: str = "current", **kwargs):
        pass

    @abstractmethod
    def _get_current_weather(self, city):
        pass

    @abstractmethod
    def _get_forecast_weather(self, city):
        pass
