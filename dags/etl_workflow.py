from datetime import datetime, timedelta

import pytz
import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from tabulate import tabulate

from api.api_key import API_KEY

# Copenhagen, Denmark coordinates
LAT = "55.6761"
LON = "12.5683"

# Default arguments for the DAG
default_args = {"start_date": days_ago(1), "retries": 1}

# Initialize the DAG
dag = DAG(
    "etl_workflow",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    description="Show weather information with date and time.",
)

# Define functions
def extract_weather_data():
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


def transform_weather_data(**context):
    """
    Transforms the weather data and adds date and time.
    """
    # Pull extracted data from XCom
    extracted_data = context["task_instance"].xcom_pull(task_ids="extract_weather_data")

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


def load_weather_data(**context):
    """
    Loads the weather data in a table format.
    """
    transformed_data = context["task_instance"].xcom_pull(
        task_ids="transform_weather_data"
    )

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


# Define the ETL tasks
extract_task = PythonOperator(
    task_id="extract_weather_data", python_callable=extract_weather_data, dag=dag
)

transform_task = PythonOperator(
    task_id="transform_weather_data",
    python_callable=transform_weather_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id="load_weather_data",
    python_callable=load_weather_data,
    provide_context=True,
    dag=dag,
)

# Set up task dependencies
extract_task >> transform_task >> load_task
