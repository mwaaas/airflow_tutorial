from airflow import DAG
from airflow.operators.slack_operator import SlackAPIPostOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.today(),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG("slack_operator_testing",
          schedule_interval=timedelta(minutes=1),
          default_args=default_args)

t1 = SlackAPIPostOperator(channel="#airflow_testing", dag=dag, task_id='task_1', token="xoxp-15492294033-15488615813-91553961473-878d4a29f770e782e9a0b303ad2b63a3")



