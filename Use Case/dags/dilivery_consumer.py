from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
import random
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def create_master_consumer(bootstrap_servers, topic_name):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=[bootstrap_servers],
        auto_offset_reset='earliest',
        group_id='admin-consumer-group'
    )

    for message in consumer:
        message_data = json.loads(message.value.decode('utf-8'))
        if message_data.get('status') == 'delivered':
            print(f"Admin: Driver {message_data.get('driver_id')} delivery completed.")


# create_driver_producer.py

def create_driver_producer(driver_id, distance, bootstrap_servers, topic_name):
    producer = KafkaProducer(
        bootstrap_servers=[bootstrap_servers],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    for i in range(distance):
        message = {
            'driver_id': driver_id,
            'status': 'en_route',
            'distance_covered': i + 1
        }
        producer.send(topic_name, value=message)
        if (i + 1) % 1000 == 0:
            print(f"Delivery Agent for {driver_id}: {i + 1} units covered")

    producer.send(topic_name, value={'driver_id': driver_id, 'status': 'delivered', 'distance_covered': distance})
    producer.flush()
    print(f"Delivery Agent for {driver_id}: Delivery completed.")



# create_driver_consumer.py

def create_driver_consumer(driver_id, bootstrap_servers, topic_name):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=[bootstrap_servers],
        auto_offset_reset='earliest',
        group_id=f'{driver_id}-consumer-group'
    )

    for message in consumer:
        message_data = json.loads(message.value.decode('utf-8'))
        if message_data.get('driver_id') == driver_id and message_data.get('status') == 'delivered':
            print(f"Customer: Driver {driver_id} delivery completed.")
            break



def fetch_new_driver_details():
    return [(f'driver{random.randint(1, 1000)}', random.randint(10000, 15000)) for _ in range(3)]

# dag.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag_id = 'drivers_management_dag'

def manage_drivers():
    new_drivers = fetch_new_driver_details()
    for driver_id, distance in new_drivers:
        create_driver_producer(driver_id, distance, 'kafka:9092', 'driver-updates')
        create_driver_consumer(driver_id, 'kafka:9092', 'driver-updates')

with DAG(dag_id, default_args=default_args, schedule_interval=timedelta(seconds=10), catchup=False) as dag:
    manage_drivers_task = PythonOperator(
        task_id='manage_drivers',
        python_callable=manage_drivers
    )
