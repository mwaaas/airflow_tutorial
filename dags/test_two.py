"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](http://pythonhosted.org/airflow/tutorial.html)
"""
from airflow import DAG
from airflow.operators import BashOperator, PythonOperator
from datetime import datetime, timedelta
import requests

seven_days_ago = datetime.today() + timedelta(minutes=1)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': seven_days_ago,
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'schedule_interval': timedelta(1),
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('testing2-dag', default_args=default_args)

def send_message():
    data = {
        "hi": [["0702729654", ""]]
    }
    url = 'http://lb.tumacredo-stag.a087b769.svc.dockerapp.io:9000/api_v1/send_sms'
    headers = {
        "Authorization": "jwt eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9pZCI6MSwiZW1haWwiOiJhZG1pbkBleGFtcGxlLmNvbSIsImV4cCI6MTQ2Njk1MDk4Mn0.wtkfgxyJ5j0vfLlptdOx_eSk41V2BUcNJIouy5DbsRQ",
        "ContentType": "application/json"
    }
    response = requests.post(url=url, json=data, headers=headers)
    print(response.content)

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = PythonOperator(
    python_callable=send_message,
    task_id="sms_4",
    dag=dag
)



t1.doc_md = """\
#### Task Documentation
You can document your task using the attributes `doc_md` (markdown),
`doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
rendered in the UI's Task Details page.
![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
"""

dag.doc_md = __doc__


t2 = PythonOperator(
    python_callable=send_message,
    task_id="sms_5",
    dag=dag
)

t3 = PythonOperator(
    python_callable=send_message,
    task_id="sms_6",
    dag=dag
)


t2.set_upstream(t1)
t3.set_upstream(t1)