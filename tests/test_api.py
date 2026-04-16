import requests
from weather.models import Weather
from weather.api import get_coordinates, get_weather_cached


def test_get_coordinates_success(monkeypatch):
    class FakeResp:
        def raise_for_status(self):
            return None

        def json(self):
            return [{"lat": "40.4168", "lon": "-3.7038", "display_name": "Madrid, España"}]

    monkeypatch.setattr("weather.api.requests.get", lambda *a, **k: FakeResp())
    coords = get_coordinates("Madrid")
    assert coords is not None
    lat, lon, name = coords
    assert abs(lat - 40.4168) < 1e-4
    assert "Madrid" in name


def test_get_weather_cached_uses_cache(monkeypatch, tmp_path):
    # simulate a requests.get that works on first call and would fail afterwards
    call = {"n": 0}

    def fake_get(*args, **kwargs):
        call["n"] += 1

        class FakeResp:
            def raise_for_status(self):
                return None

            def json(self_inner):
                if "open-meteo" in args[0]:
                    return {"current_weather": {"temperature": 10.0, "windspeed": 2.0, "weathercode": 0, "time": "2026-04-16T12:00:00Z"}}
                return []

        if call["n"] > 1:
            raise requests.RequestException("network")
        return FakeResp()

    monkeypatch.setattr("weather.api.requests.get", fake_get)

    w1 = get_weather_cached(1.0, 1.0, location_name="Loc")
    assert isinstance(w1, Weather)

    # second call should return cached result and NOT call requests.get again
    w2 = get_weather_cached(1.0, 1.0, location_name="Loc")
    assert isinstance(w2, Weather)
    assert call["n"] == 1
