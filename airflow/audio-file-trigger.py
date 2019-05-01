from datetime import datetime, timedelta, date

from airflow import DAG
from airflow.operators import PythonOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.bash_operator import BashOperator
# from airflow.contrib.sensors import GoogleCloudStorageObjectSensor
from airflow_gcs_sensor import GoogleCloudStorageObjectSensor

CONN_ID = "gcp_conn"
CDAP_CONN = "CDAP_conn"

PROJECT_ID = "datahawks-239302"

YESTERDAY = datetime.combine(
    datetime.today() - timedelta(20),
    datetime.min.time())

DEFAULT_ARGS = {
    'owner': 'datahawks',
    'start_date': YESTERDAY
}

dag = DAG(
    'audio-file-trigger',
    default_args=DEFAULT_ARGS,
    schedule_interval="@once"
)

trigger = GoogleCloudStorageObjectSensor(
    task_id='sensor',
    bucket='datahawks-storage',
    object='temp/test.txt',
    google_cloud_conn_id=CONN_ID,
    timeout=120,
    dag=dag
)

start_pipeline = SimpleHttpOperator(
    task_id='start_pipeline',
    method='POST',
    http_conn_id=CDAP_CONN,
    endpoint='v3/namespaces/default/apps/simple/workflows/DataPipelineWorkflow/start',
    headers={"Authorization": "Bearer AghjZGFwAIbvupbOWobf7ejOWuKswJcEQPaX111wfooSTr/gUo4dZdWJLvcDKSnZduuXpytWSJoJ"},
    dag=dag)

# notify = BashOperator(task_id='case_false', 
#                         bash_command='echo done',
#                         dag=dag)

trigger >> start_pipeline
