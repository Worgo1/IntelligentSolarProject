import pandas as pd
import random
from datetime import datetime, timedelta

# Define wild weather conditions for Canadian spring
extreme_weather_states = [
    {'condition': 'Sunny', 'clouds': 10, 'rain': 0, 'snow': 0},
    {'condition': 'Partly Cloudy', 'clouds': 30, 'rain': 0, 'snow': 0},
    {'condition': 'Cloudy', 'clouds': 60, 'rain': 0, 'snow': 0},
    {'condition': 'Light Rain', 'clouds': 80, 'rain': 2, 'snow': 0},
    {'condition': 'Heavy Rain', 'clouds': 90, 'rain': 15, 'snow': 0},
    {'condition': 'Thunderstorm', 'clouds': 95, 'rain': 20, 'snow': 0},
    {'condition': 'Snow Showers', 'clouds': 90, 'rain': 0, 'snow': 5},
    {'condition': 'Heavy Snow', 'clouds': 95, 'rain': 0, 'snow': 15},
    {'condition': 'Freezing Rain', 'clouds': 85, 'rain': 10, 'snow': 3},
    {'condition': 'Clear and Warm', 'clouds': 5, 'rain': 0, 'snow': 0}
]

latitude = 45.4215   # Example location (Ottawa)
longitude = -75.6972
num_hours = 720  # Simulate 30 days * 24 hours

# Start date and time
start_datetime = datetime(2024, 4, 1, 6, 0)

data = []
current_state = random.choice(extreme_weather_states)

for i in range(num_hours):
    # Occasionally switch to a different dramatic weather state
    if random.random() < 0.6:
        current_state = random.choice(extreme_weather_states)

    current_datetime = start_datetime + timedelta(hours=i)
    date_str = current_datetime.strftime('%Y-%m-%d')
    time_str = current_datetime.strftime('%H:%M')

    wind_speed = round(random.uniform(2, 25), 1)
    clouds = current_state['clouds'] + random.randint(-10, 10)
    rain_mm = round(current_state['rain'] + random.uniform(-2, 2), 1)
    rain_mm = max(rain_mm, 0)
    snow_mm = round(current_state['snow'] + random.uniform(-2, 2), 1)
    snow_mm = max(snow_mm, 0)

    entry = {
        'date': date_str,
        'time': time_str,
        'latitude': latitude,
        'longitude': longitude,
        'clouds': min(max(clouds, 0), 100),
        'wind_speed_m_s': wind_speed,
        'rain_mm': rain_mm,
        'snow_mm': snow_mm,
        'weather_condition': current_state['condition']
    }
    data.append(entry)

# Convert to DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('canadian_spring_weather.csv', index=False)

print("✅ Generated canadian_spring_weather_with_datetime.csv with hourly date and time entries.")
