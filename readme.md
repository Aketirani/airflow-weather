# Airflow DAGs Project
This project demonstrates the use of Apache Airflow for orchestrating workflows. It includes an example DAG to showcase Airflow functionalities and serves as an example of how to set up and manage tasks with Airflow.

### Project Overview
Apache Airflow is a platform to programmatically author, schedule, and monitor workflows. This project includes an example DAG that retrieves and processes weather data from the OpenWeatherMap API. It’s designed to help you understand how to set up and manage tasks within Airflow.

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
To get started with this project, ensure that you have Docker installed on your system. Follow the official [Docker installation guide](https://docs.docker.com/get-docker/) and [Docker Compose installation guide](https://docs.docker.com/compose/install/) for help with the installation process. You can also watch [Install Apache Airflow](https://www.youtube.com/watch?v=Fl64Y0p7rls).

Clone the repository to your local machine and navigate to the project's root directory to access all the necessary files and scripts.

### Requirement for Weather Data DAG

To enable the Weather Data DAG to function correctly, you'll need an API key from [OpenWeatherMap](https://openweathermap.org/api).

Follow these steps to configure your environment:

1. **Obtain an API Key**:
   - Visit [OpenWeatherMap](https://openweathermap.org/api) and sign up for an API key.

2. **Set Up API Key in Your Project**:
   - In the root directory of your project, create a folder named `api`.
   - Inside the `api` folder, create a Python file named `api_key.py`.

3. **Add Your API Key**:
   - Open the `api_key.py` file and add the following code:
     ```python
     API_KEY = "your_openweathermap_api_key_here"
     ```
   - Replace `"your_openweathermap_api_key_here"` with the actual API key you obtained from OpenWeatherMap.

This setup will ensure that your Weather Data DAG can securely access the API key needed for its operations.

### Conclusion
This project provides a foundational example of using Apache Airflow for workflow orchestration. It demonstrates basic DAG creation and task management, serving as a starting point for more complex workflows.
