# Use the official Airflow image as a parent image
FROM apache/airflow:latest

# Set the Airflow user
USER airflow

# Set the working directory in the container
WORKDIR /usr/local/airflow

# Install additional necessary packages or Python modules
RUN pip install --no-cache-dir \
    apache-airflow-providers-apache-kafka

# Install the kafka-python library
RUN pip install kafka-python


# Switch back to root user to perform any further actions
USER root
