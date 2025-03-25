import time
from weather import WeatherMonitor
from optimizer import PanelOptimizer
from controller import MotorController

def main():
    # Initialize components
    weather_monitor = WeatherMonitor()
    optimizer = PanelOptimizer()
    controller = MotorController()
    
    # Example coordinates (New York City)
    latitude = 40.7128
    longitude = -74.0060
    
    print("Starting Solar Panel Tracking System...")
    print(f"Monitoring weather for location: {latitude}, {longitude}")
    
    try:
        while True:
            # 1. Get current weather data
            weather_data = weather_monitor.get_weather_data(latitude, longitude)
            print("\nCurrent Weather Conditions:")
            print(f"Cloud Cover: {weather_data['clouds']}%")
            print(f"Wind Speed: {weather_data['wind_speed']} m/s")
            print(f"Rain: {weather_data['rain']} mm/h")
            print(f"Condition: {weather_data['weather_condition']}")
            
            # 2. Calculate optimal angles
            current_position = controller.get_current_position()
            optimal_angles = optimizer.calculate_optimal_angles(weather_data)
            
            print(f"\nOptimal angles - Tilt: {optimal_angles[0]:.1f}°, Azimuth: {optimal_angles[1]:.1f}°")
            
            # 3. Determine if movement is necessary
            movement_priority = optimizer.get_movement_priority(
                weather_data, current_position, optimal_angles
            )
            
            if movement_priority > 0.3:  # Only move if priority is high enough
                print(f"\nMoving panels (priority: {movement_priority:.2f})")
                controller.move_to_position(optimal_angles)
            else:
                print("\nSkipping movement - priority too low")
            
            # 4. Wait before next update
            print("\nWaiting for next update...")
            time.sleep(300)  # Update every 5 minutes
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nError occurred: {e}")
        controller.emergency_stop()

if __name__ == "__main__":
    main()