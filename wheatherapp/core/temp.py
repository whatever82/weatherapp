rez = {
  "latitude": 44.674866,
  "longitude": 26.070879,
  "generationtime_ms": 0.354886054992676,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "timezone_abbreviation": "GMT",
  "elevation": 110,
  "daily_units": {
    "time": "iso8601",
    "temperature_2m_max": "°C",
    "temperature_2m_min": "°C"
  },
  "daily": {
    "time": [
      "2025-05-01",
      "2025-05-02",
      "2025-05-03"
    ],
    "temperature_2m_max": [23.8, 21.2, 25.6],
    "temperature_2m_min": [8.6, 11.8, 8.9]
  }
}
location = 'Peris'

daily  = rez.get('daily', {})
measurement_keys = daily.keys()

timestamps = daily.get('time', [])


for i, date in enumerate(timestamps):
        for key in measurement_keys:
            if key != "time":  # Skip 'time' key since it's not a measurement
                value = daily[key][i]  # Get corresponding value for the timestamp
                print(
                    location,
                    key,
                    date,
                    value
                )


