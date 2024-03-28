from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from dilivery_consumer import create_master_consumer

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag_id = 'master_consumer_dag'

def start_master_consumer():
    create_master_consumer(bootstrap_servers='kafka:9092', topic_name='driver-updates')

with DAG(dag_id, default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    start_master_consumer_task = PythonOperator(
        task_id='start_master_consumer',
        python_callable=start_master_consumer
    )
