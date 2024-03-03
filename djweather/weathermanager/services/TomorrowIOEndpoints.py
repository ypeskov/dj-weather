from dataclasses import dataclass


@dataclass
class TomorrowIOEndpoints:
    REALTIME_WEATHER: str = "/weather/realtime"
