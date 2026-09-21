import asyncio

from datetime import date
from app.weather import geocode_city, get_forecast, escolher_melhor_dia, gerar_sugestao_bagagem

async def main():
    lat, lon = await geocode_city("Rio de Janeiro")
    daily = await get_forecast(lat, lon, date(2026, 9, 22), date(2026, 9, 26))

    info = escolher_melhor_dia(daily)
    print("Melhor dia:", info)

    sugestao = gerar_sugestao_bagagem(info)
    print("Sugestao de bagagem:", sugestao)

asyncio.run(main())
