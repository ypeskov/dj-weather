from dataclasses import dataclass


@dataclass
class TomorrowIOEndpoints:
    REALTIME_WEATHER: str = "/weather/realtime"
    FORECAST_WEATHER: str = "/weather/forecast"
