from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from src.extract_weather_data import WeatherExtractor
from src.load_weather_data import WeatherLoader
from src.transform_weather_data import WeatherTransformer

# Default arguments for the DAG
default_args = {"start_date": days_ago(1), "retries": 1}

# Initialize the DAG
dag = DAG(
    "etl_weather_data",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    description="Show weather information with date and time.",
)

# Initialize the classes
extractor = WeatherExtractor()
transformer = WeatherTransformer()
loader = WeatherLoader()

# Define the ETL tasks
extract_task = PythonOperator(
    task_id="extract_weather_data", python_callable=extractor.extract, dag=dag
)


def transform_wrapper(**context):
    extracted_data = context["task_instance"].xcom_pull(task_ids="extract_weather_data")
    return transformer.transform(extracted_data)


transform_task = PythonOperator(
    task_id="transform_weather_data",
    python_callable=transform_wrapper,
    provide_context=True,
    dag=dag,
)


def load_wrapper(**context):
    transformed_data = context["task_instance"].xcom_pull(
        task_ids="transform_weather_data"
    )
    loader.load(transformed_data)


load_task = PythonOperator(
    task_id="load_weather_data",
    python_callable=load_wrapper,
    provide_context=True,
    dag=dag,
)

# Set up task dependencies
extract_task >> transform_task >> load_task
