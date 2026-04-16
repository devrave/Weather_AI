# Weather CLI (sencilla)

Proyecto de ejemplo: aplicación CLI en Python que solicita una ciudad, obtiene coordenadas (Nominatim) y consulta el clima (Open-Meteo).

Instrucciones rápidas

- Crear entorno virtual:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

- Instalar dependencias:

```powershell
pip install -r requirements.txt
```

- Ejecutar la app:

```powershell
python -m weather
```

Tests

> Nota: en Windows puede ser necesario exportar `PYTHONPATH` para que `pytest` encuentre el paquete local.

- PowerShell:

```powershell
$env:PYTHONPATH = "."
pytest -q
```

- Bash/macOS/Linux:

```bash
export PYTHONPATH=.
pytest -q
```

Cache (uso y API)

Se ha añadido una función de caché en `weather/api.py`:

- `get_weather_cached(lat, lon, location_name=None, ttl=3600)` — devuelve resultados en caché si tienen menos de `ttl` segundos (por defecto 3600 = 1 hora). La caché se guarda en el directorio temporal del sistema (multiplataforma).

Ejemplo rápido en Python:

```bash
python - <<'PY'
from weather.api import get_weather_cached
w = get_weather_cached(40.4168, -3.7038, location_name="Madrid")
print(w)
PY
```

Desarrollo y pruebas

- Añadí tests para la API y la caché en `tests/test_api.py` además del test existente de formato en `tests/test_formatter.py`.
- Ejecuta `pytest` como se indica arriba para validar cambios.

Commit sugerido

Si quieres agrupar los cambios (código, tests y README) en un solo commit, usa:

```bash
git add weather/api.py tests/test_api.py Readme.md
git commit -m "feat(api): add 1-hour disk cache; docs: update README with usage and security notes; add tests"
```

Seguridad, licencia y ética

- No incluyas credenciales ni claves en el repositorio.
- Usa un `User-Agent` apropiado y respeta las políticas y límites de las APIs públicas (rate limits).
- Revisa y documenta la licencia del proyecto (p. ej. `MIT`) añadiendo un archivo `LICENSE` si procede.
- Si parte del código fue generado por IA, documenta esa contribución y revísalo manualmente antes de usar en producción.

¿Quieres que añada una sección `LICENSE` con MIT por defecto o que haga el commit por ti?
