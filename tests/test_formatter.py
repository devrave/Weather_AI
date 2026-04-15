from weather.models import Weather
from weather.formatter import format_weather


def test_format_contains_location_and_temp():
    w = Weather(temperature=21.5, windspeed=5.0, weathercode=0, time="2026-04-15T12:00:00Z", location_name="Madrid, España")
    out = format_weather(w)
    assert "Madrid" in out
    assert "21.5" in out
