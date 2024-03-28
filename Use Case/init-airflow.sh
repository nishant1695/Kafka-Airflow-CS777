#!/bin/bash

# Initialize and upgrade the database
airflow db migrate
airflow connections create-default-connections

# Create the admin user
airflow users create \
    --username admin \
    --password 1234 \
    --firstname Saurabh \
    --lastname Singh \
    --role Admin \
    --email admin@example.com

# Start the webserver
exec airflow webserver