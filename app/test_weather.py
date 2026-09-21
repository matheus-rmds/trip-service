import httpx

cidade = "Rio de Janeiro"

resp = httpx.get(
    "https://geocoding-api.open-meteo.com/v1/search",
    params={"name": cidade, "count": 1, "language": "pt"},
)
dados_cidade = resp.json()
lat = dados_cidade["results"][0]["latitude"]
lon = dados_cidade["results"][0]["longitude"]
print("Latitude/Longitude:", lat, lon)

resp2 = httpx.get(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": lat,
        "longitude": lon,
        "daily": "precipitation_probability_max,temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
        "start_date": "2026-09-22",
        "end_date": "2026-09-26",
    },
)
print("Status previsao:", resp2.status_code)
print(resp2.json())
