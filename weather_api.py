"""
Weather API Integration Module

This module provides functions to fetch real-time weather data for agricultural forecasting.
Currently implements mock data for development, with structure ready for real API integration.

Supported integrations (to be implemented):
- OpenWeatherMap API
- WeatherAPI
- AccuWeather API
"""

import requests
import json
import random
from datetime import datetime
from typing import Dict, Optional

# Mock weather data for development
MOCK_WEATHER_DATA = {
    'Andhra Pradesh': {'temp': 28.5, 'rainfall': 850, 'humidity': 68},
    'Arunachal Pradesh': {'temp': 22.2, 'rainfall': 2100, 'humidity': 75},
    'Assam': {'temp': 23.1, 'rainfall': 1800, 'humidity': 76},
    'Bihar': {'temp': 26.2, 'rainfall': 1050, 'humidity': 56},
    'Chhattisgarh': {'temp': 26.0, 'rainfall': 1200, 'humidity': 59},
    'Delhi': {'temp': 25.5, 'rainfall': 700, 'humidity': 45},
    'Goa': {'temp': 27.4, 'rainfall': 2200, 'humidity': 74},
    'Gujarat': {'temp': 27.8, 'rainfall': 750, 'humidity': 48},
    'Haryana': {'temp': 24.2, 'rainfall': 950, 'humidity': 47},
    'Himachal Pradesh': {'temp': 21.0, 'rainfall': 1100, 'humidity': 50},
    'Jharkhand': {'temp': 23.4, 'rainfall': 1350, 'humidity': 62},
    'Jammu and Kashmir': {'temp': 9.5, 'rainfall': 650, 'humidity': 52},
    'Karnataka': {'temp': 23.7, 'rainfall': 850, 'humidity': 68},
    'Kerala': {'temp': 26.8, 'rainfall': 1800, 'humidity': 80},
    'Madhya Pradesh': {'temp': 25.2, 'rainfall': 1200, 'humidity': 52},
    'Maharashtra': {'temp': 26.7, 'rainfall': 2400, 'humidity': 67},
    'Manipur': {'temp': 20.4, 'rainfall': 1300, 'humidity': 74},
    'Meghalaya': {'temp': 17.9, 'rainfall': 2800, 'humidity': 81},
    'Mizoram': {'temp': 22.9, 'rainfall': 2000, 'humidity': 77},
    'Nagaland': {'temp': 18.3, 'rainfall': 1200, 'humidity': 74},
    'Odisha': {'temp': 26.4, 'rainfall': 1450, 'humidity': 72},
    'Puducherry': {'temp': 28.1, 'rainfall': 1200, 'humidity': 75},
    'Punjab': {'temp': 24.2, 'rainfall': 950, 'humidity': 47},
    'Sikkim': {'temp': 7.5, 'rainfall': 1100, 'humidity': 73},
    'Tamil Nadu': {'temp': 27.9, 'rainfall': 1250, 'humidity': 72},
    'Telangana': {'temp': 26.1, 'rainfall': 800, 'humidity': 60},
    'Tripura': {'temp': 25.2, 'rainfall': 2100, 'humidity': 75},
    'Uttar Pradesh': {'temp': 25.8, 'rainfall': 1000, 'humidity': 52},
    'Uttarakhand': {'temp': 18.0, 'rainfall': 1300, 'humidity': 56},
    'West Bengal': {'temp': 25.8, 'rainfall': 1550, 'humidity': 74}
}

def get_current_weather(state: str, api_key: Optional[str] = None, use_mock: bool = True) -> Dict:
    """
    Fetch current weather data for a given state
    
    Args:
        state (str): Name of the state
        api_key (str, optional): API key for weather service
        use_mock (bool): Whether to use mock data (default: True)
    
    Returns:
        Dict: Weather data containing temperature, rainfall, and humidity
    """
    
    if use_mock or api_key is None:
        return get_mock_weather(state)
    else:
        # In production, replace with actual API call
        return get_openweather_data(state, api_key)

def get_mock_weather(state: str) -> Dict:
    """
    Generate mock weather data for development and testing
    
    Args:
        state (str): Name of the state
    
    Returns:
        Dict: Mock weather data
    """
    
    # Get base data for the state
    if state in MOCK_WEATHER_DATA:
        base_data = MOCK_WEATHER_DATA[state].copy()
    else:
        # Default values if state not found
        base_data = {'temp': 25.0, 'rainfall': 1000, 'humidity': 65}
    
    # Add some randomness to simulate real-time variation
    current_time = datetime.now()
    random.seed(current_time.day + current_time.hour)  # Predictable randomness based on time
    
    weather_data = {
        'avg_temp_c': round(base_data['temp'] + random.uniform(-2, 2), 1),
        'total_rainfall_mm': round(base_data['rainfall'] + random.uniform(-100, 100), 1),
        'avg_humidity_percent': round(base_data['humidity'] + random.uniform(-5, 5), 1),
        'timestamp': current_time.isoformat(),
        'source': 'mock_data',
        'state': state
    }
    
    # Ensure realistic bounds
    weather_data['avg_temp_c'] = max(0, min(50, weather_data['avg_temp_c']))
    weather_data['total_rainfall_mm'] = max(0, weather_data['total_rainfall_mm'])
    weather_data['avg_humidity_percent'] = max(10, min(100, weather_data['avg_humidity_percent']))
    
    return weather_data

def get_openweather_data(state: str, api_key: str) -> Dict:
    """
    Fetch weather data from OpenWeatherMap API
    
    Args:
        state (str): Name of the state
        api_key (str): OpenWeatherMap API key
    
    Returns:
        Dict: Weather data from OpenWeatherMap
    
    Note:
        This is a placeholder implementation. In production, you would:
        1. Get API key from environment variables
        2. Handle API rate limits
        3. Implement proper error handling and retries
        4. Cache results to avoid excessive API calls
    """
    
    try:
        # OpenWeatherMap API endpoint
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        # Parameters for the API call
        params = {
            'q': f"{state},IN",  # Assuming Indian states
            'appid': api_key,
            'units': 'metric'
        }
        
        # Make API request
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant weather information
        weather_data = {
            'avg_temp_c': data['main']['temp'],
            'total_rainfall_mm': data.get('rain', {}).get('1h', 0) * 24,  # Convert hourly to daily estimate
            'avg_humidity_percent': data['main']['humidity'],
            'timestamp': datetime.now().isoformat(),
            'source': 'openweathermap',
            'state': state
        }
        
        return weather_data
        
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        # Fallback to mock data
        return get_mock_weather(state)
    except KeyError as e:
        print(f"Unexpected API response format: {e}")
        return get_mock_weather(state)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return get_mock_weather(state)

def get_weather_forecast(state: str, days: int = 7, api_key: Optional[str] = None) -> Dict:
    """
    Get weather forecast for multiple days (placeholder implementation)
    
    Args:
        state (str): Name of the state
        days (int): Number of days to forecast
        api_key (str, optional): API key for weather service
    
    Returns:
        Dict: Weather forecast data
    """
    
    # For now, return mock forecast data
    current_weather = get_current_weather(state, api_key)
    
    forecast = {
        'state': state,
        'forecast_days': days,
        'daily_forecast': []
    }
    
    # Generate mock forecast for each day
    for day in range(days):
        day_forecast = {
            'day': day + 1,
            'avg_temp_c': current_weather['avg_temp_c'] + random.uniform(-3, 3),
            'total_rainfall_mm': current_weather['total_rainfall_mm'] * random.uniform(0.5, 1.5),
            'avg_humidity_percent': current_weather['avg_humidity_percent'] + random.uniform(-10, 10)
        }
        
        # Apply bounds
        day_forecast['avg_temp_c'] = max(0, min(50, day_forecast['avg_temp_c']))
        day_forecast['total_rainfall_mm'] = max(0, day_forecast['total_rainfall_mm'])
        day_forecast['avg_humidity_percent'] = max(10, min(100, day_forecast['avg_humidity_percent']))
        
        forecast['daily_forecast'].append(day_forecast)
    
    return forecast

def validate_weather_data(weather_data: Dict) -> bool:
    """
    Validate weather data for completeness and realistic values
    
    Args:
        weather_data (Dict): Weather data to validate
    
    Returns:
        bool: True if data is valid, False otherwise
    """
    
    required_fields = ['avg_temp_c', 'total_rainfall_mm', 'avg_humidity_percent']
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in weather_data:
            return False
    
    # Check if values are realistic
    temp = weather_data['avg_temp_c']
    rainfall = weather_data['total_rainfall_mm']
    humidity = weather_data['avg_humidity_percent']
    
    if not (-10 <= temp <= 55):  # Temperature range for India
        return False
    
    if not (0 <= rainfall <= 5000):  # Rainfall range
        return False
    
    if not (10 <= humidity <= 100):  # Humidity range
        return False
    
    return True

# Example usage and testing functions
def main():
    """Test weather API functions"""
    test_states = ['Maharashtra', 'Punjab', 'Kerala', 'Rajasthan']
    
    print("Testing Weather API Functions")
    print("=" * 50)
    
    for state in test_states:
        print(f"\nWeather for {state}:")
        weather = get_current_weather(state)
        print(f"Temperature: {weather['avg_temp_c']}Â°C")
        print(f"Rainfall: {weather['total_rainfall_mm']}mm")
        print(f"Humidity: {weather['avg_humidity_percent']}%")
        print(f"Valid data: {validate_weather_data(weather)}")

if __name__ == "__main__":
    main()
