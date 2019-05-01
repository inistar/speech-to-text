from datetime import datetime, timedelta, date

from airflow import DAG
from airflow.operators import PythonOperator

CONN_ID = "gcp_conn"

PROJECT_ID = "datahawks-239302"

YESTERDAY = datetime.combine(
    datetime.today() - timedelta(20),
    datetime.min.time())

DEFAULT_ARGS = {
    'owner': 'datahawks',
    'start_date': YESTERDAY
}

TRIGGER_DAG = DAG(
    'audio-file-trigger',
    default_args=DEFAULT_ARGS,
    schedule_interval="@once"
)

def logic():
    print("Hello World")

T1 = PythonOperator(
    task_id='trigger',
    python_callable=logic,
    provide_context=True,
    dag=TRIGGER_DAG
)

T1