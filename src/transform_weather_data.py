from datetime import datetime, timedelta

import pytz


class WeatherTransformer:
    def transform(self, extracted_data):
        """
        Transforms the weather data and adds date and time.
        """
        # Convert sunrise and sunset times from API to local time
        timezone_offset = extracted_data["timezone"]
        offset_hours = timezone_offset // 3600
        offset_minutes = (timezone_offset % 3600) // 60

        # Calculate the timezone offset for local conversion
        timezone = pytz.FixedOffset(offset_hours * 60 + offset_minutes)

        # Convert API times to local time
        sunrise_time = datetime.fromtimestamp(
            extracted_data["sunrise"], tz=pytz.utc
        ).astimezone(timezone)
        sunset_time = datetime.fromtimestamp(
            extracted_data["sunset"], tz=pytz.utc
        ).astimezone(timezone)

        # Format timezone for display
        sign = "+" if offset_hours >= 0 else "-"
        gmt_timezone = f"GMT{sign}{abs(offset_hours):02}:{abs(offset_minutes):02}"

        # Get the current time and add the GMT offset
        current_time = datetime.now()
        adjusted_time = current_time + timedelta(hours=offset_hours)
        formatted_time = adjusted_time.strftime("%Y-%m-%d %H:%M:%S")

        # Update extracted data with formatted times and GMT timezone
        extracted_data["sunrise"] = sunrise_time.strftime("%H:%M:%S")
        extracted_data["sunset"] = sunset_time.strftime("%H:%M:%S")
        extracted_data["timezone"] = gmt_timezone
        extracted_data["datetime"] = formatted_time

        # Print the transformed data
        print("TRANSFORMED DATA:", extracted_data)
        return extracted_data
