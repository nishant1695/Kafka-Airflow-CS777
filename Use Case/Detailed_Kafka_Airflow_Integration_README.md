
# Kafka and Airflow Integration Project

## Overview
This project demonstrates the integration of Apache Kafka with Apache Airflow to build a batch delivery system. It showcases real-time data streaming with Kafka and workflow orchestration with Airflow.

## Prerequisites
- Docker
- Docker Compose
- Git

## Setup Instructions

### 1. Environment Preparation
Ensure Docker, Docker Compose, and Git are installed on your system.

### 2. Clone the Repository
Clone the project repository to obtain the necessary Docker and DAG configurations.
```bash
git clone <repository-url>
cd <project-directory>
```

### 3. Docker Configuration
Navigate to the project directory and build the Docker image for Airflow, then start the services.
```bash
docker build -t my-airflow-image .
docker-compose up
```

### 4. Verify the Installation
Check if all Docker containers are running correctly.
```bash
docker ps
```

## Usage

### Accessing Airflow
Open `http://localhost:8080` in a web browser to access the Airflow web interface.

### Running the DAG
Find the `master_consumer_dag` & 'drivers_management_dag' in the Airflow UI and trigger it manually to start processing.

### Monitoring and Logs
Use the Airflow UI to monitor the DAG's progress and view task logs for detailed execution information.

## Project Structure
- `Dockerfile`: Docker configuration for Airflow image.
- `docker-compose.yml`: Docker Compose setup for Airflow, Kafka, Zookeeper, and PostgreSQL.
- `dags/`: Directory containing DAG files for Airflow.
- `logs/`: Directory for storing Airflow logs.

## Conclusion
This setup exemplifies how Kafka and Airflow can be integrated for efficient data processing and workflow management in a scalable architecture.
