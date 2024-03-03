from abc import abstractmethod


class WeatherService:
    def __init__(self):
        self.api_key = "1111111111"

    @abstractmethod
    def get_current_weather(self, city):
        pass
