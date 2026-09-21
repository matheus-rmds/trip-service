from datetime import date
from typing import Tuple

import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

async def geocode_city(city: str) -> Tuple[float, float]:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "pt"},
        )
        resp.raise_for_status()
        data = resp.json()

    if not data.get("results"):
        raise ValueError(f"City '{city}' not found")

    result = data["results"][0]
    return result["latitude"], result["longitude"]

async def get_forecast(lat: float, lon: float, start_date: date, end_date: date) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            FORECAST_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "precipitation_probability_max,temperature_2m_max,temperature_2m_min",
                "timezone": "auto",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )
        resp.raise_for_status()
        return resp.json()["daily"]

def choose_best_day(daily: dict) -> dict:
    days = daily["time"]
    rain = daily["precipitation_probability_max"]
    temp_max = daily["temperature_2m_max"]
    temp_min = daily["temperature_2m_min"]

    best_index = min(range(len(days)), key=lambda i: rain[i])

    return {
        "best_day": date.fromisoformat(days[best_index]),
        "rain_chance": rain[best_index],
        "temp_max": temp_max[best_index],
        "temp_min": temp_min[best_index],
    }

def generate_packing_suggestion(info: dict) -> str:
    items = []
    if info["rain_chance"] >= 40:
        items.append("guarda-chuva")
    if info["temp_max"] >= 28:
        items.append("protetor solar")
    if info["temp_min"] <= 15:
        items.append("casaco")
    if not items:
        items.append("roupas leves, sem itens especiais necessarios")
    return ", ".join(items)
