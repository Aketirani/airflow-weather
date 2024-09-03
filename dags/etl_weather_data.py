from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from src.extract_weather_data import WeatherExtractor
from src.load_weather_data import WeatherLoader
from src.transform_weather_data import WeatherTransformer


class WeatherETL:
    """
    Class to encapsulate the ETL process for weather data
    """

    def __init__(self, dag: DAG) -> None:
        """
        Initialize the WeatherETL class with the DAG

        :param dag: DAG instance to associate with the tasks
        """
        self.dag = dag
        self.extractor = WeatherExtractor()
        self.transformer = WeatherTransformer()
        self.loader = WeatherLoader()
        self._create_tasks()

    def _create_tasks(self) -> None:
        """
        Create and define the ETL tasks for the DAG
        """
        self.extract_task = PythonOperator(
            task_id="extract_weather_data",
            python_callable=self._extract_weather,
            provide_context=True,
            dag=self.dag,
        )

        self.transform_task = PythonOperator(
            task_id="transform_weather_data",
            python_callable=self._transform_weather,
            provide_context=True,
            dag=self.dag,
        )

        self.load_task = PythonOperator(
            task_id="load_weather_data",
            python_callable=self._load_weather,
            provide_context=True,
            dag=self.dag,
        )

        # Set up task dependencies
        self.extract_task >> self.transform_task >> self.load_task

    def _extract_weather(self, **kwargs) -> dict:
        """
        Extract weather data

        :param kwargs: Context dictionary provided by Airflow
        :return: dict, extracted weather data
        """
        return self.extractor.extract()

    def _transform_weather(self, **kwargs) -> dict:
        """
        Transform the extracted weather data

        :param kwargs: Context dictionary provided by Airflow
        :return: dict, transformed weather data
        """
        extracted_data = kwargs["task_instance"].xcom_pull(
            task_ids="extract_weather_data"
        )
        return self.transformer.transform(extracted_data)

    def _load_weather(self, **kwargs) -> None:
        """
        Load the transformed weather data

        :param kwargs: Context dictionary provided by Airflow
        """
        transformed_data = kwargs["task_instance"].xcom_pull(
            task_ids="transform_weather_data"
        )
        self.loader.load(transformed_data)


# Default arguments for the DAG
default_args = {
    "start_date": days_ago(1),
    "retries": 1,
}

# Initialize the DAG
dag = DAG(
    "etl_weather_data",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    description="ETL DAG to extract, transform, and load weather information with date and time.",
)

# Initialize and configure the ETL process
weather_etl = WeatherETL(dag)
