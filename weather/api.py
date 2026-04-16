"""Cliente HTTP simple para geocoding (Nominatim) y Open-Meteo."""
from __future__ import annotations

import requests
import json
import time
import tempfile
from pathlib import Path
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


def _cache_dir() -> Path:
    d = Path(tempfile.gettempdir()) / "weather_cli_cache"
    try:
        d.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return d


def _cache_path(lat: float, lon: float) -> Path:
    # keep filenames short and filesystem-friendly
    name = f"{lat:.4f}_{lon:.4f}.json"
    return _cache_dir() / name


def _load_cached(lat: float, lon: float, ttl: int) -> dict | None:
    path = _cache_path(lat, lon)
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
        ts = payload.get("ts")
        if ts is None:
            return None
        if time.time() - float(ts) > float(ttl):
            return None
        return payload.get("weather")
    except Exception:
        return None


def _save_cached(lat: float, lon: float, weather: Weather) -> None:
    path = _cache_path(lat, lon)
    payload = {
        "ts": time.time(),
        "weather": {
            "temperature": weather.temperature,
            "windspeed": weather.windspeed,
            "weathercode": weather.weathercode,
            "time": weather.time,
            "location_name": weather.location_name,
        },
    }
    tmp = path.with_suffix(".tmp")
    try:
        with tmp.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh)
        tmp.replace(path)
    except Exception:
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass


def get_weather_cached(lat: float, lon: float, location_name: str | None = None, ttl: int = 3600) -> Weather | None:
    """Devuelve datos en caché si siguen siendo válidos; si no, consulta la API y guarda en caché.

    - `ttl` en segundos (por defecto 3600 = 1 hora).
    - Caché en disco en el directorio temporal del sistema (multiplataforma).
    """
    data = _load_cached(lat, lon, ttl)
    if data:
        try:
            return Weather(**data)
        except Exception:
            pass
    w = get_weather(lat, lon, location_name)
    if w:
        _save_cached(lat, lon, w)
    return w
