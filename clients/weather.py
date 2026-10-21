from clients.http import NotFoundError, ServiceError, get_with_retry, parse_json, require

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

DESCRIPTIONS = {
    0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "fog", 48: "depositing rime fog",
    51: "light drizzle", 53: "moderate drizzle", 55: "dense drizzle",
    56: "light freezing drizzle", 57: "dense freezing drizzle",
    61: "slight rain", 63: "moderate rain", 65: "heavy rain",
    66: "light freezing rain", 67: "heavy freezing rain",
    71: "slight snowfall", 73: "moderate snowfall", 75: "heavy snowfall", 77: "snow grains",
    80: "slight rain showers", 81: "moderate rain showers", 82: "violent rain showers",
    85: "slight snow showers", 86: "heavy snow showers",
    95: "thunderstorm", 96: "thunderstorm with slight hail",
    97: "heavy thunderstorm", 99: "thunderstorm with heavy hail",
}


def get_weather(city):
    geo = parse_json(get_with_retry(GEO_URL, params={"name": city, "count": 1}))
    if not geo.get("results"):
        raise NotFoundError(f"город {city} не найден")
    place = geo["results"][0]
    require(place, "latitude", "longitude")

    params = {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": "temperature_2m,weather_code",
    }
    forecast = parse_json(get_with_retry(FORECAST_URL, params=params))
    require(forecast, "current")
    current = forecast["current"]
    require(current, "temperature_2m", "weather_code")
    if not isinstance(current["temperature_2m"], (int, float)):
        raise ServiceError("температура пришла не числом")

    return {
        "temp_c": current["temperature_2m"],
        "description": DESCRIPTIONS.get(current["weather_code"], ""),
    }