from datetime import datetime, timedelta

import pytz


class WeatherTransformer:
    """
    This class is used to transform weather data
    """

    def __init__(self) -> None:
        """
        Initialize the WeatherTransformer class
        """
        pass

    def transform(self, extracted_data: dict) -> dict:
        """
        Transforms the weather data by converting API times to local time and adding date and time information

        :param extracted_data: dict, the extracted weather data from the API
        :return: dict, transformed weather data with added date and time information
        """
        timezone_offset = extracted_data["timezone"]
        offset_hours, offset_minutes = self._calculate_timezone_offset(timezone_offset)
        timezone = pytz.FixedOffset(offset_hours * 60 + offset_minutes)

        extracted_data["sunrise"] = self._convert_to_local_time(
            extracted_data["sunrise"], timezone
        ).strftime("%H:%M:%S")
        extracted_data["sunset"] = self._convert_to_local_time(
            extracted_data["sunset"], timezone
        ).strftime("%H:%M:%S")
        extracted_data["timezone"] = self._format_timezone(offset_hours, offset_minutes)
        extracted_data["datetime"] = self._get_formatted_datetime(offset_hours)

        # Print the transformed data
        print("TRANSFORMED DATA:", extracted_data)
        return extracted_data

    def _calculate_timezone_offset(self, timezone_offset: int) -> tuple:
        """
        Calculate the timezone offset in hours and minutes

        :param timezone_offset: int, the timezone offset in seconds
        :return: tuple, (offset_hours, offset_minutes)
        """
        offset_hours = timezone_offset // 3600
        offset_minutes = (timezone_offset % 3600) // 60
        return offset_hours, offset_minutes

    def _convert_to_local_time(
        self, timestamp: int, timezone: pytz.FixedOffset
    ) -> datetime:
        """
        Convert a Unix timestamp to a local time given a timezone

        :param timestamp: int, the Unix timestamp
        :param timezone: pytz.FixedOffset, the timezone for conversion
        :return: datetime, the local time
        """
        return datetime.fromtimestamp(timestamp, tz=pytz.utc).astimezone(timezone)

    def _format_timezone(self, offset_hours: int, offset_minutes: int) -> str:
        """
        Format the timezone for display

        :param offset_hours: int, timezone offset in hours
        :param offset_minutes: int, timezone offset in minutes
        :return: str, formatted timezone
        """
        sign = "+" if offset_hours >= 0 else "-"
        return f"GMT{sign}{abs(offset_hours):02}:{abs(offset_minutes):02}"

    def _get_formatted_datetime(self, offset_hours: int) -> str:
        """
        Get the current date and time adjusted by the GMT offset

        :param offset_hours: int, GMT offset in hours
        :return: str, formatted current date and time
        """
        current_time = datetime.now()
        adjusted_time = current_time + timedelta(hours=offset_hours)
        return adjusted_time.strftime("%Y-%m-%d %H:%M:%S")
