#imports
import uuid
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow_test',
    'start_date': datetime(2024, 3, 15, 21, 00)
}

#Getting Data From API
def get_data():
    import requests

    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res['results'][0]

    return res

#Getting specific fields and formatting data for sending to the producer
def format_data(res):
    data = {}
    location = res['location']
    data['id'] = str(uuid.uuid4())
    data['first_name'] = str(res['name']['first'])
    data['last_name'] = str(res['name']['last'])
    data['gender'] = str(res['gender'])
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = str(location['postcode'])
    data['email'] = str(res['email'])
    data['username'] = str(res['login']['username'])
    data['dob'] = str(res['dob']['date'])
    data['registered_date'] = str(res['registered']['date'])
    data['phone'] = str(res['phone'])
    data['picture'] = str(res['picture']['medium'])

    return data

def stream_data():
    import json
    from kafka import KafkaProducer
    import time
    import logging

    #Defining producer and the address of kafka server 
    producer = KafkaProducer(bootstrap_servers=['10.0.0.143:9092'], max_block_ms=5000)
    curr_time = time.time()

    
    while True:
        if time.time() > curr_time + 15: #15 seconds
            break
        try:
            res = get_data()
            res = format_data(res)

            print("data formatted!")
            topic_name = "hello_world"
            data = json.dumps(str(res)).encode('utf-8')
            producer.send(topic_name, value=data)
        except Exception as e:
            logging.error(f'An error occured: {e}')
            continue

#Defining DAG
with DAG('user_automation',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data
    )
