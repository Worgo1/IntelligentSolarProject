from typing import Tuple
import time

class MotorController:
    def __init__(self):
        self.current_tilt = 0.0
        self.current_azimuth = 180.0  # Assuming starting position facing south
        self.movement_speed = 5.0  # degrees per second
        self.is_moving = False
    
    def move_to_position(self, target_angles: Tuple[float, float]) -> bool:
        """
        Simulate moving the panel to target position.
        
        Args:
            target_angles (Tuple[float, float]): Target (tilt, azimuth) angles
            
        Returns:
            bool: True if movement successful, False otherwise
        """
        target_tilt, target_azimuth = target_angles
        
        try:
            self.is_moving = True
            
            # Calculate required movements
            tilt_diff = abs(target_tilt - self.current_tilt)
            azimuth_diff = abs(target_azimuth - self.current_azimuth)
            
            # Simulate movement time
            total_movement = max(tilt_diff, azimuth_diff)
            movement_time = total_movement / self.movement_speed
            
            # Simulate the movement
            print(f"Moving panel: Tilt {self.current_tilt:.1f}° → {target_tilt:.1f}°, "
                  f"Azimuth {self.current_azimuth:.1f}° → {target_azimuth:.1f}°")
            print(f"Estimated movement time: {movement_time:.1f} seconds")
            
            # Simulate gradual movement
            time.sleep(min(movement_time, 0.1))  # Cap simulation time for demo
            
            # Update current position
            self.current_tilt = target_tilt
            self.current_azimuth = target_azimuth
            
            print("Movement completed")
            return True
            
        except Exception as e:
            print(f"Error during movement: {e}")
            return False
            
        finally:
            self.is_moving = False
    
    def get_current_position(self) -> Tuple[float, float]:
        """
        Get current panel position.
        
        Returns:
            Tuple[float, float]: Current (tilt, azimuth) angles
        """
        return (self.current_tilt, self.current_azimuth)
    
    def emergency_stop(self) -> None:
        """
        Emergency stop function to halt all movement immediately.
        """
        if self.is_moving:
            print("Emergency stop triggered!")
            self.is_moving = False 