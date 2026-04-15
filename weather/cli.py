"""Interfaz de línea de comandos simple para solicitar ciudad y mostrar el clima."""
from __future__ import annotations

import argparse
from .api import get_coordinates, get_weather
from .formatter import format_weather


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="weather", description="Consulta el clima por ciudad")
    parser.add_argument("--city", "-c", help="Nombre de la ciudad", required=False)
    args = parser.parse_args(argv)

    if args.city:
        city = args.city
    else:
        city = input("Introduce el nombre de la ciudad: ").strip()
        if not city:
            print("No se ha indicado ciudad. Saliendo.")
            return 1

    coords = get_coordinates(city)
    if not coords:
        print(f"No se encontraron coordenadas para '{city}'.")
        return 2

    lat, lon, display_name = coords
    weather = get_weather(lat, lon, location_name=display_name)
    if not weather:
        print("No se pudo obtener el clima. Intenta más tarde.")
        return 3

    print(format_weather(weather))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
