from tabulate import tabulate


class WeatherLoader:
    def load(self, transformed_data):
        """
        Loads the weather data in a table format.
        """
        # Define the headers and rows for the table
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
            [
                "Wind Gust (m/s)",
                f"{transformed_data['wind_gust'] if transformed_data['wind_gust'] != 'N/A' else 'N/A'}",
            ],
            ["Rain (last 1h) (mm)", transformed_data["rain_1h"]],
            ["Snow (last 1h) (mm)", transformed_data["snow_1h"]],
            ["Sunrise", transformed_data["sunrise"]],
            ["Sunset", transformed_data["sunset"]],
            ["Timezone", transformed_data["timezone"]],
            ["Date and Time", transformed_data["datetime"]],
        ]

        # Print the table
        table = tabulate(rows, headers=headers, tablefmt="grid")
        print("LOADED DATA:\n")
        print(table)
