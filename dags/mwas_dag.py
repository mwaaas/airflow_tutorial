"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](http://pythonhosted.org/airflow/tutorial.html)
"""
from airflow import DAG
from airflow.operators import BashOperator, PythonOperator
from datetime import datetime, timedelta
import requests
import json

seven_days_ago = datetime.combine(datetime.today() - timedelta(7),
                                  datetime.min.time())

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

dag = DAG('mwaside-dag', default_args=default_args)

def send_message(message):
    url = 'http://lb.tumacredo-stag.a087b769.svc.dockerapp.io:9000/api_v1/send_sms'

    payload = {u'sender_id': None,
               u'message_data': {message: [[u'0702729654', u'']]},
               u'calculated_cost': 1}
    payload = json.dumps(payload)

    headers = {
        'content-type': "application/json",
        'authorization': "Basic YWRtaW46eXoycnNNY2FqM1VKM2RhUnN3QmQ="
    }

    response = requests.post(url, data=payload, headers=headers)

    print(response.text)

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = PythonOperator(
    python_callable=send_message,
    op_args="sms one",
    task_id="sms_one",
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
op_args="sms one",
    task_id="sms_two",
    dag=dag
)

t3 = PythonOperator(
    python_callable=send_message,
    task_id="sms_three",
    dag=dag
)


t2.set_upstream(t1)
t3.set_upstream(t1)