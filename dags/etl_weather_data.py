from airflow import DAG
from airflow.exceptions import AirflowException
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

        self.extract_task >> self.transform_task >> self.load_task

    def _extract_weather(self, **kwargs) -> dict:
        """
        Extract weather data

        :param kwargs: Context dictionary provided by Airflow
        :return: dict, extracted weather data
        """
        try:
            return self.extractor.extract()
        except Exception as e:
            self.log.error(f"Weather data extraction failed: {str(e)}")
            raise AirflowException(f"Extraction task failed: {str(e)}")

    def _transform_weather(self, **kwargs) -> dict:
        """
        Transform the extracted weather data

        :param kwargs: Context dictionary provided by Airflow
        :return: dict, transformed weather data
        """
        try:
            extracted_data = kwargs["task_instance"].xcom_pull(
                task_ids="extract_weather_data"
            )
            return self.transformer.transform(extracted_data)
        except Exception as e:
            self.log.error(f"Weather data transformation failed: {str(e)}")
            raise AirflowException(f"Transformation task failed: {str(e)}")

    def _load_weather(self, **kwargs) -> None:
        """
        Load the transformed weather data and write to CSV

        :param kwargs: Context dictionary provided by Airflow
        """
        try:
            transformed_data = kwargs["task_instance"].xcom_pull(
                task_ids="transform_weather_data"
            )
            self.loader.load(transformed_data)
        except Exception as e:
            self.log.error(f"Weather data loading failed: {str(e)}")
            raise AirflowException(f"Loading task failed: {str(e)}")


default_args = {
    "start_date": days_ago(1),
    "retries": 1,
}

dag = DAG(
    "etl_weather_data",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    description="ETL DAG to extract, transform, and load weather information with date and time.",
)

weather_etl = WeatherETL(dag)
