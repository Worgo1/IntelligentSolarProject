import time
import csv
from weather import WeatherMonitor
from optimizer import PanelOptimizer
from controller import MotorController

def main():
    # Initialize components
    latitude = 45.421466
    longitude =  -75.70240879573106
    weather_monitor = WeatherMonitor("canadian_spring_weather.csv")
    optimizer = PanelOptimizer(latitude, longitude)
    controller = MotorController()
    
    # Open the CSV file to log results
    with open('solar_panel_log.csv', 'w', newline='') as csvfile:
        fieldnames = ['date', 'time', 'clouds', 'wind_speed', 'rain', 'snow', 
                      'weather_condition', 'optimal_tilt', 'optimal_azimuth']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row
        
        print("Starting Solar Panel Tracking System...")
        
        try:
            while True:
                # 1. Get current weather data
                weather_data = weather_monitor.get_weather_data()
                print("\nCurrent Weather Conditions:")
                print(f"Cloud Cover: {weather_data['clouds']}%")
                print(f"Wind Speed: {weather_data['wind_speed']} m/s")
                print(f"Rain: {weather_data['rain']} mm/h")
                print(f"Condition: {weather_data['weather_condition']}")
                
                # 2. Calculate optimal angles
                current_position = controller.get_current_position()
                optimal_angles = optimizer.calculate_optimal_angles(weather_data)
                
                print(f"\nOptimal angles - Tilt: {optimal_angles[0]:.1f}°, Azimuth: {optimal_angles[1]:.1f}°")
                
                # 3. Log the weather data and calculated angles
                log_data = {
                    'date': weather_data['date'],
                    'time': weather_data['time'],
                    'clouds': weather_data['clouds'],
                    'wind_speed': weather_data['wind_speed'],
                    'rain': weather_data['rain'],
                    'snow': weather_data['snow'],
                    'weather_condition': weather_data['weather_condition'],
                    'optimal_tilt': optimal_angles[0],
                    'optimal_azimuth': optimal_angles[1]
                }
                writer.writerow(log_data)  # Log the data in CSV

                # 4. Determine if movement is necessary
                movement_priority = optimizer.get_movement_priority(
                    weather_data, current_position, optimal_angles
                )
                
                if movement_priority > 0.3:  # Only move if priority is high enough
                    print(f"\nMoving panels (priority: {movement_priority:.2f})")
                    controller.move_to_position(optimal_angles)
                else:
                    print("\nSkipping movement - priority too low")
                
        except KeyboardInterrupt:
            print("\nShutting down...")
        except Exception as e:
            print(f"\nError occurred: {e}")
            controller.emergency_stop()

if __name__ == "__main__":
    main()
