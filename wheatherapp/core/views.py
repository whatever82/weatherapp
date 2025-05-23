from django.shortcuts import render
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from django.utils.timezone import make_aware
from datetime import datetime

from .models import Location, HistoricalWeather
from .utils import get_location, get_historical_weather

async def location(request, location):

    result = await get_location(location)

    for entry in result.get('results', []):
        await sync_to_async(Location.objects.get_or_create)(
            id=entry.get('id'),
            name=entry.get('name'),
            latitude=entry.get('latitude'),
            longitude=entry.get('longitude'),
            elevation=entry.get('elevation'),
            country_code=entry.get('country_code'),
            timezone=entry.get('timezone'),
            country_id=entry.get('country_id'),
            country=entry.get('country'),
            population=entry.get('population'),
        )

    return JsonResponse({"message": "Locations processed!", "count": len(result.get('results', []))})


async def history(request, latitude, longitude, start_date, end_date):

    rez = await get_historical_weather(
        latitude=float(latitude),
        longitude=float(longitude),
        start_date=start_date,
        end_date=end_date
    )

    location_qs = await sync_to_async(Location.objects.filter)(latitude=latitude, longitude=longitude)
    location = await sync_to_async(location_qs.first)()
    
    if not location:
        return {'message': 'location not found in the database'}
    
    daily = rez.get('daily', {})
    measurement_keys = daily.keys()
    timestamps = daily.get('time', [])

    await sync_to_async(HistoricalWeather.objects.filter(location=location, measurement__in=measurement_keys).delete)()

    records_to_insert = []

    for i, date in enumerate(timestamps):
        aware_date = make_aware(datetime.strptime(date, "%Y-%m-%d"))

        for key in measurement_keys:
            if key != 'time':
                value = daily[key][i]

                records_to_insert.append(
                    HistoricalWeather(
                        location=location,
                        measurement=key,
                        time=aware_date,
                        value=value
                    )
                )

    if records_to_insert:
        await sync_to_async(HistoricalWeather.objects.bulk_create)(records_to_insert)


    return JsonResponse({"message": "records uploaded!", "count": len(records_to_insert)})