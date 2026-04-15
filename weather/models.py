from dataclasses import dataclass


@dataclass
class Weather:
    temperature: float
    windspeed: float
    weathercode: int
    time: str
    location_name: str | None = None
