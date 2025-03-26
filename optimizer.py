import math
import pandas as pd
from datetime import datetime
from typing import Tuple
import pvlib
from pvlib import solarposition

class PanelOptimizer:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude
        self.min_angle = 0  # Minimum tilt angle (horizontal)
        self.max_angle = 90  # Maximum tilt angle (vertical)
        self.safe_angle = 0  # Safe position for extreme weather (horizontal)
    
    def calculate_optimal_angles(self, weather_data: dict) -> Tuple[float, float]:
        """
        Calculate optimal tilt and azimuth angles based on weather conditions and time.
        
        Args:
            weather_data (dict): Weather data from WeatherMonitor
            current_datetime (datetime): The current date and time
            
        Returns:
            Tuple[float, float]: (tilt_angle, azimuth_angle) in degrees
        """
        # If extreme weather, return safe position
        current_datetime = pd.to_datetime(weather_data.get('date') + " " + weather_data.get('time') + ':00')
        if self._should_use_safe_position(weather_data):
            return (self.safe_angle, 0.0)
        
        # Use pvlib to calculate the solar position
        solar_pos = self.calculate_solar_position(current_datetime)
        
        # Solar Azimuth and Elevation
        azimuth = solar_pos['azimuth'].iloc[0]  # Azimuth in degrees
        elevation = solar_pos['elevation'].iloc[0]  # Elevation in degrees
        
        # Adjust tilt angle based on weather and solar elevation
        base_tilt = elevation  # Base tilt angle is the solar elevation
        cloud_factor = weather_data['clouds'] / 100.0
        
        # If it's cloudy, increase tilt to capture more diffuse light
        if cloud_factor > 0.6:
            adjusted_tilt = base_tilt + (base_tilt * 0.2)  # Increase tilt by 20% on cloudy days
        else:
            adjusted_tilt = base_tilt
        
        # Ensure tilt is within min/max bounds
        tilt = max(self.min_angle, min(self.max_angle, adjusted_tilt))
        
        # Return the adjusted tilt and azimuth
        return (tilt, azimuth)
    
    def calculate_solar_position(self, current_datetime: datetime) -> pd.DataFrame:
        """
        Calculate the solar position (azimuth and elevation) based on the time and location.
        
        Args:
            current_datetime (datetime): The current date and time
            
        Returns:
            pd.DataFrame: A DataFrame containing solar azimuth and elevation
        """
        # Convert datetime to the format used by pvlib (Timestamp)
        current_time = pd.Timestamp(current_datetime)
        
        # Create a pandas datetime index for pvlib
        times = pd.DatetimeIndex([current_time])
        
        # Use pvlib to calculate solar position
        solar_pos = solarposition.get_solarposition(times, self.latitude, self.longitude)
        
        return solar_pos
    
    def _should_use_safe_position(self, weather_data: dict) -> bool:
        """
        Determine if panels should be moved to safe position.
        
        Args:
            weather_data (dict): Weather data from WeatherMonitor
            
        Returns:
            bool: True if safe position should be used
        """
        return (
            weather_data['wind_speed'] > 15.0 or  # High wind
            weather_data['rain'] > 5.0 or  # Significant rain
            weather_data['weather_condition'] in ['Thunderstorm', 'Tornado', 'Hurricane']
        )
    
    def get_movement_priority(self, weather_data: dict, current_angles: Tuple[float, float],
                            target_angles: Tuple[float, float]) -> float:
        """
        Calculate priority of movement based on potential gain vs energy cost.
        
        Args:
            weather_data (dict): Current weather conditions
            current_angles (Tuple[float, float]): Current (tilt, azimuth)
            target_angles (Tuple[float, float]): Target (tilt, azimuth)
            
        Returns:
            float: Priority score (0-1), where 1 is highest priority
        """
        if self._should_use_safe_position(weather_data):
            return 1.0  # Always move to safe position when needed
            
        angle_diff = math.sqrt(
            (target_angles[0] - current_angles[0])**2 +
            (target_angles[1] - current_angles[1])**2
        )
        
        # If the difference is very small, don't move
        if angle_diff < 5.0:
            return 0.0
            
        # Calculate priority based on weather conditions and angle difference
        cloud_factor = 1.0 - (weather_data['clouds'] / 100.0)
        priority = cloud_factor * (angle_diff / 90.0)
        
        return max(0.0, min(1.0, priority))
