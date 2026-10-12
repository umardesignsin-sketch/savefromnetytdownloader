"""Bounded integrations for translation and official US forecast data."""

import html
import math
import re
import threading
import time
from urllib.parse import urlsplit

import requests


class GrowthServiceError(ValueError):
    def __init__(self, message, code="source_unavailable", status=503):
        super().__init__(message)
        self.code = code
        self.status = status


LANGUAGES = {"en", "es", "fr"}
NWS_HEADERS = {"User-Agent": "SaveFromNet.fun weather tool (https://savefromnet.fun/contact)",
               "Accept": "application/geo+json"}
_weather_cache = {}
_cache_lock = threading.Lock()


def translate_text(text, source, target):
    if not isinstance(text, str) or not text.strip() or len(text) > 500:
        raise GrowthServiceError("Enter 1 to 500 characters of text.", "invalid_text", 400)
    if source not in LANGUAGES or target not in LANGUAGES or source == target:
        raise GrowthServiceError("Choose two different supported languages.", "invalid_language", 400)
    try:
        response = requests.get("https://api.mymemory.translated.net/get",
                                params={"q": text.strip(), "langpair": f"{source}|{target}"},
                                headers={"User-Agent": "SaveFromNet.fun/1.0"}, timeout=8)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise GrowthServiceError("Translation is temporarily unavailable. Please try again later.") from exc
    if not isinstance(data, dict) or str(data.get("responseStatus")) != "200":
        raise GrowthServiceError("The translation service could not process this text. Try a shorter phrase.",
                                 "translation_unavailable", 502)
    response_data = data.get("responseData")
    if not isinstance(response_data, dict):
        raise GrowthServiceError("The translation service returned an invalid response.",
                                 "translation_unavailable", 502)
    translated = html.unescape(str(response_data.get("translatedText") or "")).strip()
    if not translated or translated.upper().startswith("MYMEMORY WARNING"):
        raise GrowthServiceError("Translation is unavailable right now. Please try again later.",
                                 "translation_unavailable", 503)
    return {"translation": translated[:2000], "source": source, "target": target,
            "provider": "MyMemory"}


def _public_nws_url(value):
    if not isinstance(value, str):
        raise GrowthServiceError("The forecast source returned an invalid link.")
    try:
        parsed = urlsplit(value)
        allowed = (parsed.scheme == "https" and parsed.hostname == "api.weather.gov" and
                   parsed.port is None and not parsed.username and not parsed.password and
                   parsed.path.startswith("/gridpoints/") and not parsed.query and not parsed.fragment)
    except ValueError:
        allowed = False
    if not allowed:
        raise GrowthServiceError("The forecast source returned an invalid link.")
    return value


def us_forecast(zip_code):
    if not isinstance(zip_code, str) or not re.fullmatch(r"[0-9]{5}", zip_code):
        raise GrowthServiceError("Enter a five-digit US ZIP code.", "invalid_zip", 400)
    now = time.monotonic()
    with _cache_lock:
        cached = _weather_cache.get(zip_code)
        if cached and cached[0] > now:
            return cached[1]
    try:
        location_response = requests.get(f"https://api.zippopotam.us/us/{zip_code}", timeout=6)
        if location_response.status_code == 404:
            raise GrowthServiceError("That US ZIP code was not found.", "unknown_zip", 404)
        location_response.raise_for_status()
        location = location_response.json()
        place = location["places"][0]
        latitude = float(place["latitude"])
        longitude = float(place["longitude"])
        if not (math.isfinite(latitude) and math.isfinite(longitude) and
                -90 <= latitude <= 90 and -180 <= longitude <= 180):
            raise ValueError("invalid coordinates")
        points_response = requests.get(f"https://api.weather.gov/points/{latitude:.4f},{longitude:.4f}",
                                       headers=NWS_HEADERS, timeout=8)
        if points_response.status_code == 404:
            raise GrowthServiceError("The National Weather Service has no forecast for this ZIP code.",
                                     "outside_forecast_area", 404)
        points_response.raise_for_status()
        forecast_url = _public_nws_url(points_response.json()["properties"]["forecast"])
        forecast_response = requests.get(forecast_url, headers=NWS_HEADERS, timeout=8)
        forecast_response.raise_for_status()
        forecast = forecast_response.json()["properties"]
        periods = forecast["periods"][:6]
        if not periods:
            raise ValueError("missing forecast periods")
        result = {
            "zip": zip_code,
            "location": f'{place["place name"]}, {place["state abbreviation"]}',
            "updated": forecast.get("updated"),
            "source_url": forecast_url,
            "periods": [{
                "name": str(period.get("name") or "Forecast")[:60],
                "temperature": int(period["temperature"]),
                "temperature_unit": str(period.get("temperatureUnit") or "F")[:2],
                "short_forecast": str(period.get("shortForecast") or "")[:120],
                "detailed_forecast": str(period.get("detailedForecast") or "")[:700],
                "wind_speed": str(period.get("windSpeed") or "")[:40],
                "wind_direction": str(period.get("windDirection") or "")[:10],
            } for period in periods],
        }
    except GrowthServiceError:
        raise
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError, AttributeError) as exc:
        raise GrowthServiceError("The weather source is temporarily unavailable. Please try again later.") from exc
    with _cache_lock:
        _weather_cache[zip_code] = (now + 600, result)
        if len(_weather_cache) > 256:
            for key, (expiry, _) in list(_weather_cache.items()):
                if expiry <= now:
                    del _weather_cache[key]
            if len(_weather_cache) > 256:
                _weather_cache.pop(next(iter(_weather_cache)))
    return result
