# Airflow DAGs Project
This project demonstrates the use of Apache Airflow for orchestrating workflows. It includes a sample DAG to showcase basic Airflow functionalities and serves as an example of how to set up and manage tasks with Airflow.

### Project Overview
Apache Airflow is a platform to programmatically author, schedule, and monitor workflows. This project includes a simple DAG that prints a welcome message and the current date. It’s designed to help you understand how to set up and manage tasks within Airflow.

### Structure
```
├── dags                        <-- DAGs Folder
|   └── *.py                    <-- DAGs Files
|
├── logs                        <-- Logs Folder
|
├── .env                        <-- Environment Variables
|
├── .gitignore                  <-- Git Ignore Configuration
|
├── .pre-commit-config.yaml     <-- Pre-Commit Hooks Configuration
|
├── docker-compose.yaml         <-- Docker Compose Configuration
|
├── README.md                   <-- Project Overview and Setup Instructions
|
├── requirements.txt            <-- Python Package Requirements
```

### Installation
To get started with this project, ensure that you have Docker installed on your system. Follow the official [Docker installation guide](https://docs.docker.com/get-docker/) and [Docker Compose installation guide](https://docs.docker.com/compose/install/) for help with the installation process. You can also watch [Install Apache Airflow](https://www.youtube.com/watch?v=Fl64Y0p7rls).

Clone the repository to your local machine and navigate to the project's root directory to access all the necessary files and scripts.

### Conclusion
This project provides a foundational example of using Apache Airflow for workflow orchestration. It demonstrates basic DAG creation and task management, serving as a starting point for more complex workflows.
