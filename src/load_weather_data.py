import csv
import os

from tabulate import tabulate


class WeatherLoader:
    """
    This class is used to load weather data
    """

    def __init__(self) -> None:
        """
        Initialize the WeatherLoader class with the path to the CSV file
        """
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.csv_path = os.path.join(root_dir, "data", "weather_data.csv")

    def _format_wind_gust(self, wind_gust: str) -> str:
        """
        Formats the wind gust value for display.

        :param wind_gust: str, the wind gust value or 'N/A'
        :return: str, formatted wind gust value
        """
        return wind_gust if wind_gust != "N/A" else "N/A"

    def _generate_rows(self, transformed_data: dict) -> list:
        """
        Generates the rows for the table and CSV file from the transformed weather data

        :param transformed_data: dict, the transformed weather data
        :return: list of lists, the rows for the table and CSV
        """
        return [
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

    def _generate_table(self, transformed_data: dict) -> str:
        """
        Generates a table formatted string from the transformed weather data

        :param transformed_data: dict, the transformed weather data
        :return: str, the table formatted string
        """
        headers = ["Parameter", "Value"]
        rows = self._generate_rows(transformed_data)
        return tabulate(rows, headers=headers, tablefmt="grid")

    def _write_to_csv(self, transformed_data: dict) -> None:
        """
        Writes the transformed weather data to a CSV file

        :param transformed_data: dict, the transformed weather data
        """
        rows = self._generate_rows(transformed_data)
        with open(self.csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Parameter", "Value"])
            writer.writerows(rows)
        print(f"Data written to CSV file at: {self.csv_path}")

    def load(self, transformed_data: dict) -> None:
        """
        Loads the weather data in a table format and writes to a CSV file

        :param transformed_data: dict, the transformed weather data
        """
        table = self._generate_table(transformed_data)
        print("LOADED DATA:\n")
        print(table)
        self._write_to_csv(transformed_data)
