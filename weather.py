import os
import requests
from dotenv import load_dotenv

class WeatherMonitor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        if not self.api_key:
            raise ValueError("WeatherAPI key not found in .env file")
        self.base_url = "http://api.weatherapi.com/v1/current.json"
    
    def get_weather_data(self, latitude: float, longitude: float) -> dict:
        """
        Fetch current weather data for the given coordinates.
        
        Args:
            latitude (float): Location latitude
            longitude (float): Location longitude
            
        Returns:
            dict: Weather data including cloud cover, wind speed, and rain
        """
        params = {
            'q': f"{latitude},{longitude}",
            'key': self.api_key,
            'aqi': 'no'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            weather_info = {
                'clouds': data['current']['cloud'],  # Cloud coverage in %
                'wind_speed': data['current']['wind_kph'] / 3.6,  # Convert km/h to m/s
                'rain': data['current']['precip_mm'],  # Rain volume in mm
                'weather_condition': data['current']['condition']['text']
            }
            return weather_info
            
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return {
                'clouds': 0,
                'wind_speed': 0,
                'rain': 0,
                'weather_condition': 'Clear'
            }
    
    def is_extreme_weather(self, weather_data: dict) -> bool:
        """
        Determine if current weather conditions are extreme.
        
        Args:
            weather_data (dict): Weather data from get_weather_data
            
        Returns:
            bool: True if conditions are extreme, False otherwise
        """
        return (
            weather_data['wind_speed'] > 20.0 or  # Wind speed > 20 m/s
            weather_data['rain'] > 10.0 or  # Heavy rain > 10mm/hour
            any(condition in weather_data['weather_condition'].lower() 
                for condition in ['thunder', 'storm', 'tornado', 'hurricane'])
        ) 