import requests

from api.api_key import API_KEY


class WeatherExtractor:
    """
    This class is used to extract weather information using the OpenWeatherMap API
    """

    def __init__(self, lat: str = "55.6761", lon: str = "12.5683") -> None:
        """
        Initialize the class with latitude and longitude coordinates

        :param lat: str, latitude for the location
        :param lon: str, longitude for the location
        """
        self.lat = lat
        self.lon = lon

    def extract(self) -> dict:
        """
        Extracts the current weather information using the OpenWeatherMap API

        :return: dict, extracted weather data
        """
        response = self._fetch_weather_data()
        weather_data = response.json()
        extracted_data = self._parse_weather_data(weather_data)
        print("EXTRACTED DATA:", extracted_data)
        return extracted_data

    def _fetch_weather_data(self) -> requests.Response:
        """
        Fetches the weather data from the OpenWeatherMap API

        :return: requests.Response, the API response object
        """
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={API_KEY}&units=metric"
        return requests.get(url)

    def _parse_weather_data(self, weather_data: dict) -> dict:
        """
        Parses the weather data from the API response

        :param weather_data: dict, the raw weather data from the API
        :return: dict, parsed weather data
        """
        return {
            "city": weather_data["name"],
            "country": weather_data["sys"]["country"],
            "temperature": weather_data["main"]["temp"],
            "feels_like": weather_data["main"]["feels_like"],
            "temp_min": weather_data["main"]["temp_min"],
            "temp_max": weather_data["main"]["temp_max"],
            "humidity": weather_data["main"]["humidity"],
            "weather_description": weather_data["weather"][0]["description"],
            "wind_speed": weather_data["wind"]["speed"],
            "wind_gust": weather_data.get("wind", {}).get("gust", "N/A"),
            "rain_1h": weather_data.get("rain", {}).get("1h", "0"),
            "snow_1h": weather_data.get("snow", {}).get("1h", "0"),
            "sunrise": weather_data["sys"]["sunrise"],
            "sunset": weather_data["sys"]["sunset"],
            "timezone": weather_data["timezone"],
        }
