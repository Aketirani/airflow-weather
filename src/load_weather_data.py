from tabulate import tabulate


class WeatherLoader:
    """
    This class is used to load weather data
    """

    def __init__(self) -> None:
        """
        Initialize the WeatherLoader class
        """
        pass

    def load(self, transformed_data: dict) -> None:
        """
        Loads the weather data in a table format

        :param transformed_data: dict, the transformed weather data
        """
        table = self._generate_table(transformed_data)
        print("LOADED DATA:\n")
        print(table)

    def _generate_table(self, transformed_data: dict) -> str:
        """
        Generates a table formatted string from the transformed weather data

        :param transformed_data: dict, the transformed weather data
        :return: str, the table formatted string
        """
        headers = ["Parameter", "Value"]
        rows = [
            ["City", transformed_data["city"]],
            ["Country", transformed_data["country"]],
            ["Temperature (°C)", f"{transformed_data['temperature']:.2f}"],
            ["Feels Like (°C)", f"{transformed_data['feels_like']:.2f}"],
            ["Min Temperature (°C)", f"{transformed_data['temp_min']:.2f}"],
            ["Max Temperature (°C)", f"{transformed_data['temp_max']:.2f}"],
            ["Humidity (%)", transformed_data["humidity"]],
            ["Weather Description", transformed_data["weather_description"]],
            ["Wind Speed (m/s)", f"{transformed_data['wind_speed']:.2f}"],
            ["Wind Gust (m/s)", self._format_wind_gust(transformed_data["wind_gust"])],
            ["Rain (last 1h) (mm)", transformed_data["rain_1h"]],
            ["Snow (last 1h) (mm)", transformed_data["snow_1h"]],
            ["Sunrise", transformed_data["sunrise"]],
            ["Sunset", transformed_data["sunset"]],
            ["Timezone", transformed_data["timezone"]],
            ["Date and Time", transformed_data["datetime"]],
        ]
        return tabulate(rows, headers=headers, tablefmt="grid")

    def _format_wind_gust(self, wind_gust: str) -> str:
        """
        Formats the wind gust value for display.

        :param wind_gust: str, the wind gust value or 'N/A'
        :return: str, formatted wind gust value
        """
        return wind_gust if wind_gust != "N/A" else "N/A"
