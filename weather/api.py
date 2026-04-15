"""Cliente HTTP simple para geocoding (Nominatim) y Open-Meteo."""
from __future__ import annotations

import requests
from . import config
from .models import Weather


def get_coordinates(city: str) -> tuple[float, float, str] | None:
    params = {"q": city, "format": "json", "limit": 1}
    try:
        r = requests.get(config.NOMINATIM_URL, params=params, timeout=config.DEFAULT_TIMEOUT, headers={"User-Agent": "weather-cli/0.1"})
        r.raise_for_status()
        data = r.json()
        if not data:
            return None
        item = data[0]
        return float(item["lat"]), float(item["lon"]), item.get("display_name")
    except requests.RequestException:
        return None


def get_weather(lat: float, lon: float, location_name: str | None = None) -> Weather | None:
    params = {"latitude": lat, "longitude": lon, "current_weather": True, "timezone": "auto"}
    try:
        r = requests.get(config.OPEN_METEO_URL, params=params, timeout=config.DEFAULT_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        cw = data.get("current_weather")
        if not cw:
            return None
        return Weather(
            temperature=cw.get("temperature"),
            windspeed=cw.get("windspeed"),
            weathercode=cw.get("weathercode"),
            time=cw.get("time"),
            location_name=location_name,
        )
    except requests.RequestException:
        return None
