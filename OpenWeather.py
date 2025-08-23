import requests
import json
import time
import os

def get_california_cities():
    """Return a list of major cities in California"""
    # List of major California cities with their coordinates
    # You might want to expand this list with more cities
    california_cities = [
        {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
        {"name": "San Diego", "lat": 32.7157, "lon": -117.1611},
        {"name": "San Jose", "lat": 37.3382, "lon": -121.8863},
        {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194},
        {"name": "Fresno", "lat": 36.7378, "lon": -119.7871},
        {"name": "Sacramento", "lat": 38.5816, "lon": -121.4944},
        {"name": "Long Beach", "lat": 33.7701, "lon": -118.1937},
        {"name": "Oakland", "lat": 37.8044, "lon": -122.2712},
        {"name": "Bakersfield", "lat": 35.3733, "lon": -119.0187},
        {"name": "Anaheim", "lat": 33.8366, "lon": -117.9143},
        {"name": "Santa Ana", "lat": 33.7455, "lon": -117.8677},
        {"name": "Riverside", "lat": 33.9806, "lon": -117.3755},
        {"name": "Stockton", "lat": 37.9577, "lon": -121.2908},
        {"name": "Irvine", "lat": 33.6846, "lon": -117.8265},
        {"name": "Chula Vista", "lat": 32.6401, "lon": -117.0842},
        {"name": "Fremont", "lat": 37.5485, "lon": -121.9886},
        {"name": "San Bernardino", "lat": 34.1083, "lon": -117.2898},
        {"name": "Modesto", "lat": 37.6391, "lon": -120.9969},
        {"name": "Fontana", "lat": 34.0922, "lon": -117.4350},
        {"name": "Oxnard", "lat": 34.1975, "lon": -119.1771}
    ]
    return california_cities

def get_temperature_data(api_key, cities):
    """Fetch temperature data for all cities using OpenWeather API"""
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    weather_data = []
    
    for i, city in enumerate(cities):
        # Construct the API request URL
        params = {
            'lat': city['lat'],
            'lon': city['lon'],
            'appid': api_key,
            'units': 'imperial'  # Use 'metric' for Celsius
        }
        
        try:
            # Make the API request
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            data = response.json()
            
            # Extract the relevant information
            city_weather = {
                'city': city['name'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'pressure': data['main']['pressure'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind']['deg'],
                'cloudiness': data['clouds']['all'],
                'visibility': data['visibility'],
                'sunrise': data['sys']['sunrise'],
                'description': data['weather'][0]['description'],
                'timestamp': data['dt']
            }
            
            weather_data.append(city_weather)
            print(f"Fetched data for {city['name']}: {city_weather['temperature']}°F")
            
            # Add a small delay between requests to respect API rate limits
            if i < len(cities) - 1:  # Don't sleep after the last request
                time.sleep(1)  # Free tier allows up to 60 calls per minute
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {city['name']}: {e}")
        except KeyError as e:
            print(f"Unexpected response format for {city['name']}: {e}")
    
    return weather_data

def save_to_json(data, filename):
    """Save weather data to a JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

def main():
    # Get your API key from environment variable or replace with your actual key
    api_key = '7e4f6a0fb4d39473a8c8bf853718f04c'
    
    if not api_key:
        print("Please set the OPENWEATHER_API_KEY environment variable")
        print("Or replace the api_key variable with your actual API key")
        return
    
    # Get the list of California cities
    cities = get_california_cities()
    print(f"Fetching weather data for {len(cities)} California cities...")
    
    # Fetch temperature data
    weather_data = get_temperature_data(api_key, cities)
    
    # Save to JSON file
    save_to_json(weather_data, 'california_temperatures.json')
    
    # Print summary
    print(f"\nSuccessfully retrieved data for {len(weather_data)} out of {len(cities)} cities")

if __name__ == "__main__":
    main()