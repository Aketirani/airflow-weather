# Weather Data Pipeline with Apache Airflow
Apache Airflow is a platform designed to manage and automate complex workflows through programmatic scheduling and monitoring. It empowers users to define workflows as Directed Acyclic Graphs (DAGs), which represent a series of tasks and their dependencies. Each DAG outlines the sequence in which tasks are executed, ensuring that they run in the correct order and adhere to specified dependencies.

### Project Overview
This project showcases the use of Apache Airflow to orchestrate an ETL (Extract, Transform, Load) pipeline focused on weather data. It provides a practical example of how Airflow can be employed to automate the retrieval of weather information from the OpenWeatherMap API, process and transform the data, and present it in a structured format.

### Structure
```
├── api                         <-- API Folder
|   └── api_key.py              <-- API Key Configuration
|
├── dags                        <-- DAGs Folder
|   └── *.py                    <-- DAGs Files
|
├── logs                        <-- Logs Folder
|
├── .env                        <-- Environment Variables
|
├── .gitignore                  <-- Git Ignore Configuration
|
├── .pre-commit-config.yaml     <-- Pre-Commit Configuration
|
├── docker-compose.yaml         <-- Docker Compose Configuration
|
├── README.md                   <-- You Are Here
|
├── requirements.txt            <-- Package Requirements
```

### Installation
To set up this project, follow these steps:

1. **Install Docker and Docker Compose:**
   - Follow the official [Docker installation guide](https://docs.docker.com/get-docker/) and [Docker Compose installation guide](https://docs.docker.com/compose/install/).
   - You can also watch [Install Apache Airflow](https://www.youtube.com/watch?v=Fl64Y0p7rls).

2. **Clone the Repository:**
   - Clone this repository to your local machine:
     ```bash
     git clone https://github.com/yourusername/airflow-weather.git
     cd airflow-weather
     ```

3. **Configure API Key:**
   - Obtain an API key from [OpenWeatherMap](https://openweathermap.org/api).
   - Create a folder named `api` in the project root.
   - Inside the `api` folder, create a file named `api_key.py` with the following content:
     ```python
     API_KEY = "your_openweathermap_api_key_here"
     ```

4. **Start the Airflow Cluster:**
   - Run the following commands to start the Airflow services using Docker Compose:
     ```bash
     docker-compose build
     docker-compose up
     ```

### Conclusion
This project provides a foundational example of using Apache Airflow for workflow orchestration. It demonstrates basic DAG creation and task management, serving as a starting point for more complex workflows.
