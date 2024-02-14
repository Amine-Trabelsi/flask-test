import requests
from datetime import datetime, timedelta
import random

class WeatherAPI:
    def __init__(self, api_key='YOUR_YANDEX_API_KEY', use_fake_api=True):
        self.api_key = api_key
        self.use_fake_api = use_fake_api
        self.base_url = 'https://api.weather.yandex.ru/v2/informers'
        self.headers = {'X-Yandex-API-Key': self.api_key}

        # In-memory cache to store temperature data with city as the key
        self.weather_cache = {}

    def fetch_weather(self, city):
        # If using the fake API, delegate to the fake weather fetching method
        if self.use_fake_api:
            return self._fetch_fake_weather(city)

        # Check if the weather data for the city is in the cache and not older than 10 minutes
        if city in self.weather_cache and (datetime.now() - self.weather_cache[city]['timestamp']).total_seconds() < 600:
            return self.weather_cache[city]['temperature']

        # Fetch weather data from Yandex API
        params = {'lat': '55.7558', 'lon': '37.6176', 'lang': 'en_US'}  # Replace with actual coordinates

        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            data = response.json()

            if response.status_code == 200:
                temperature = data['fact']['temp']

                # Update the cache with the new temperature and timestamp
                self.weather_cache[city] = {
                    'temperature': temperature,
                    'timestamp': datetime.now(),
                }

                return temperature
            else:
                print(f"Failed to fetch weather data. Status code: {response.status_code}")
                return None

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def _fetch_fake_weather(self, city):
        # Check if the weather data for the city is in the cache and not older than 10 minutes
        if city in self.weather_cache and (datetime.now() - self.weather_cache[city]['timestamp']).total_seconds() < 600:
            return self.weather_cache[city]['temperature']

        # Generate a random temperature as a fake API call
        temperature = round(random.uniform(-10, 30), 2)

        # Update the cache with the new temperature and timestamp
        self.weather_cache[city] = {
            'temperature': temperature,
            'timestamp': datetime.now(),
        }

        return temperature

"""
# Example usage:
api_key = 'YOUR_YANDEX_API_KEY'
weather_api = WeatherAPI(api_key, use_fake_api=True)

city_temperature_real = weather_api.fetch_weather('Moscow')
print(f'Real temperature in Moscow: {city_temperature_real}')
"""