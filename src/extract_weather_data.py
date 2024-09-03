import requests

from api.api_key import API_KEY

# Copenhagen, Denmark coordinates
LAT = "55.6761"
LON = "12.5683"


class WeatherExtractor:
    def extract(self):
        """
        Extracts the current weather information using the OpenWeatherMap API.
        """
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        weather_data = response.json()

        extracted_data = {
            "city": "Copenhagen",
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
        print("EXTRACTED DATA:", extracted_data)
        return extracted_data
