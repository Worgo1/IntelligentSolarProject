import pandas as pd

class WeatherMonitor:
    def __init__(self, csv_file_path: str):
        """
        Initialize WeatherMonitor with a CSV file instead of API.
        Args:
            csv_file_path (str): Path to the CSV file containing weather data
        """
        self.weather_data = pd.read_csv(csv_file_path)
        self.index = 0  # Track current row in the CSV
        self.data_length = len(self.weather_data)
        if self.data_length == 0:
            raise ValueError("Weather data CSV is empty.")
    
    def get_weather_data(self) -> dict:
        """
        Fetch the next weather data entry from the CSV.
        Returns:
            dict: Weather data including clouds, wind speed, rain, snow, condition
        """
        if self.index >= self.data_length:
            print("Reached end of data. Looping back to start.")
            self.index = 0  # Optional: loop around, or raise StopIteration if preferred

        row = self.weather_data.iloc[self.index]
        self.index += 1

        weather_info = {
            'date': row['date'],
            'time': row['time'],
            'clouds': row['clouds'],
            'wind_speed': row['wind_speed_m_s'],
            'rain': row.get('rain_mm', 0),  # in case rain_mm column exists
            'snow': row.get('snow_mm', 0),  # if included in CSV
            'weather_condition': row['weather_condition']
        }

        return weather_info
    
    def is_extreme_weather(self, weather_data: dict) -> bool:
        """
        Determine if current weather conditions are extreme.
        Args:
            weather_data (dict): Weather data from get_weather_data
        Returns:
            bool: True if conditions are extreme, False otherwise
        """
        return (
            weather_data['wind_speed'] > 20.0 or
            weather_data['rain'] > 10.0 or
            weather_data.get('snow', 0) > 10.0 or
            any(condition in weather_data['weather_condition'].lower()
                for condition in ['thunder', 'storm', 'tornado', 'hurricane', 'snow'])
        )
