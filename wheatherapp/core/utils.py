import httpx
import asyncio

async def get_location(name: str):
    geocoding_api = f"https://geocoding-api.open-meteo.com/v1/search?name={name}&count=10&language=en&format=json"

    async with httpx.AsyncClient() as client:
        rez = await client.get(geocoding_api)
    
    return rez.json()

async def get_historical_weather(latitude: float, longitude: float, start_date: str, end_date: str):
    url = "https://archive-api.open-meteo.com/v1/archive"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_max", "temperature_2m_min"]
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    
    data = response.json()

    return data