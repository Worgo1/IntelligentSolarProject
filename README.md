# Intelligent Solar Panel Tracking System

This system provides intelligent control for solar panels by adapting to real-time weather conditions. It optimizes panel orientation while protecting against extreme weather conditions.

## Features

- Real-time weather monitoring using OpenWeatherMap API
- Dynamic panel orientation optimization
- Energy-saving mode during unfavorable conditions
- Extreme weather protection
- Modular design architecture

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your OpenWeatherMap API key:
```
OPENWEATHER_API_KEY=your_api_key_here
```

3. Run the main program:
```bash
python solar_tracker/main.py
```

## Project Structure

- `solar_tracker/` - Main package directory
  - `weather.py` - Weather data retrieval module
  - `optimizer.py` - Panel orientation optimization logic
  - `controller.py` - Motor control simulation
  - `main.py` - Main program entry point 