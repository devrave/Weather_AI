"""Formatos de salida legibles para consola."""
from .models import Weather


WEATHER_CODE_MAP = {
    0: "Despejado",
    1: "Principalmente despejado",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Niebla",
    48: "Depósitos de escarcha",
    51: "Llovizna ligera",
    61: "Lluvia ligera",
    71: "Nieve ligera",
    80: "Chubascos",
}


def format_weather(w: Weather) -> str:
    code_desc = WEATHER_CODE_MAP.get(w.weathercode, f"Código {w.weathercode}")
    loc = w.location_name or "(ubicación desconocida)"
    return (
        f"Clima para {loc}\n"
        f"Hora: {w.time}\n"
        f"Temperatura: {w.temperature} °C\n"
        f"Viento: {w.windspeed} km/h\n"
        f"Condición: {code_desc}\n"
    )
