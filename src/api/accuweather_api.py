import requests

from config.config import config


class AccuWeatherAPI:
    def __init__(self):
        pass

    def _get(self, url: str) -> dict:
        response = requests.get(url=url)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f"incorrect request, response with status code {response.status_code}")
        if not response.json():
            raise requests.exceptions.InvalidJSONError("no json in response")
        return response.json()[0]

    def _get_location_key_by_text(self, location_name: str) -> str:
        url = f"{config.api.location_url}?apikey={config.api.api_key}&q={location_name}"
        response = self._get(url)
        return response.get("Key", "")

    def _get_weather_by_location_key(self, location_key: str) -> dict:
        url = f"{config.api.weather_url}{location_key}?apikey={config.api.api_key}&details=true"
        return self._get(url)

    def get_weather(self, location_name: str) -> dict:
        location_key = self._get_location_key_by_text(location_name)
        weather_data = self._get_weather_by_location_key(location_key)
        return weather_data
