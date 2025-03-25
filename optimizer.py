import math
from typing import Tuple

class PanelOptimizer:
    def __init__(self):
        # Default parameters
        self.min_angle = 0  # Minimum tilt angle (horizontal)
        self.max_angle = 90  # Maximum tilt angle (vertical)
        self.safe_angle = 0  # Safe position for extreme weather (horizontal)
    
    def calculate_optimal_angles(self, weather_data: dict) -> Tuple[float, float]:
        """
        Calculate optimal tilt and azimuth angles based on weather conditions.
        
        Args:
            weather_data (dict): Weather data from WeatherMonitor
            
        Returns:
            Tuple[float, float]: (tilt_angle, azimuth_angle) in degrees
        """
        # If extreme weather, return safe position
        if self._should_use_safe_position(weather_data):
            return (self.safe_angle, 0.0)
        
        # Base angle calculation (simplified for demo)
        # In a real implementation, this would also consider:
        # - Sun position (based on time, date, and location)
        # - Direct vs. diffuse radiation models
        # - Historical performance data
        
        cloud_factor = weather_data['clouds'] / 100.0
        wind_factor = min(1.0, weather_data['wind_speed'] / 20.0)
        
        # On cloudy days, a more horizontal angle might be better for diffuse light
        base_tilt = 45.0  # Optimal angle for many locations
        adjusted_tilt = base_tilt * (1 - 0.3 * cloud_factor)  # Reduce angle when cloudy
        
        # Limit the angle based on wind conditions
        if wind_factor > 0.5:
            adjusted_tilt *= (1 - (wind_factor - 0.5))
        
        # Ensure angles are within bounds
        tilt = max(self.min_angle, min(self.max_angle, adjusted_tilt))
        azimuth = 180.0  # Assuming south-facing panels in northern hemisphere
        
        return (tilt, azimuth)
    
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