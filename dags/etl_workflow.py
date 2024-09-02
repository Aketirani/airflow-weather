from datetime import datetime, timedelta, timezone

import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# OpenWeatherMap API key
API_KEY = "9fdba5c02164c7b046fdc5c29db4d683"

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
    description="A simple ETL workflow to show weather data with date and time.",
)

# Define functions
def extract_weather_data():
    """
    Extract weather data function.
    This function fetches the current weather information using the OpenWeatherMap API.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    weather_data = response.json()

    extracted_data = {
        "city": "Copenhagen",
        "country": weather_data["sys"]["country"],
        "temperature": weather_data["main"]["temp"],
        "temp_min": weather_data["main"]["temp_min"],
        "temp_max": weather_data["main"]["temp_max"],
        "humidity": weather_data["main"]["humidity"],
        "weather_description": weather_data["weather"][0]["description"],
        "wind_speed": weather_data["wind"]["speed"],
        "sunrise": weather_data["sys"]["sunrise"],
        "sunset": weather_data["sys"]["sunset"],
        "timezone": weather_data["timezone"],
    }
    print("Weather data extracted:", extracted_data)
    return extracted_data


def transform_weather_data(**context):
    """
    Transform weather data function.
    This function adds the current date and time to the weather data,
    formats the sunrise and sunset times, and converts the timezone offset
    to GMT format.
    """
    extracted_data = context["task_instance"].xcom_pull(task_ids="extract_weather_data")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Convert Unix timestamps to HH:MM:SS format, considering the timezone
    timezone_offset = timedelta(seconds=extracted_data["timezone"])
    sunrise_time = (
        datetime.fromtimestamp(extracted_data["sunrise"], tz=timezone.utc)
        + timezone_offset
    )
    sunset_time = (
        datetime.fromtimestamp(extracted_data["sunset"], tz=timezone.utc)
        + timezone_offset
    )

    # Convert timezone offset to GMT format
    offset_hours = extracted_data["timezone"] // 3600
    offset_minutes = (extracted_data["timezone"] % 3600) // 60
    sign = "+" if offset_hours >= 0 else "-"
    human_readable_timezone = (
        f"GMT{sign}{abs(offset_hours):02}:{abs(offset_minutes):02}"
    )

    # Update extracted data with formatted times and GMT timezone
    extracted_data["sunrise"] = sunrise_time.strftime("%H:%M:%S")
    extracted_data["sunset"] = sunset_time.strftime("%H:%M:%S")
    extracted_data["datetime"] = current_time
    extracted_data["timezone"] = human_readable_timezone

    print(
        "Transformed data with datetime, sunrise, sunset, and timezone:", extracted_data
    )
    return extracted_data


def load_weather_data(**context):
    """
    Load weather data function.
    This function prints the final weather data with date, time, and formatted sunrise/sunset times.
    """
    transformed_data = context["task_instance"].xcom_pull(
        task_ids="transform_weather_data"
    )
    print("Loading weather data:", transformed_data)


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
