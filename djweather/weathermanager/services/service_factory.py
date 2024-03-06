from .WeatherService import WeatherService
from .TomorrowIOService import TomorrowIOService

available_services = {
    "TomorrowIO": TomorrowIOService,
}

service_name = "TomorrowIO"


def get_weather_service() -> WeatherService:
    if service_name not in available_services:
        raise Exception(f"Service {service_name} not available.")
    return available_services.get(service_name)()
