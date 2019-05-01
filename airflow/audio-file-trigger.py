from datetime import datetime, timedelta, date

from airflow import DAG
from airflow.operators import PythonOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.bash_operator import BashOperator

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

T1 = SimpleHttpOperator(
    task_id='start_pipeline',
    method='POST',
    http_conn_id=CDAP_CONN,
    endpoint='v3/namespaces/default/apps/simple/workflows/DataPipelineWorkflow/start',
    headers={"Authorization": "Bearer AghjZGFwAIbvupbOWobf7ejOWuKswJcEQPaX111wfooSTr/gUo4dZdWJLvcDKSnZduuXpytWSJoJ"},
    dag=dag)

# start_cmd = "CURL http://104.155.164.61:11015/v3/namespaces/default/apps/simple/workflows/DataPipelineWorkflow/status -H 'Authorization: Bearer AghjZGFwAIbvupbOWobf7ejOWuKswJcEQPaX111wfooSTr/gUo4dZdWJLvcDKSnZduuXpytWSJoJ'"
# start_pipeline = BashOperator(task_id='start_pipeline', 
#                         bash_command=start_cmd,
#                         dag=dag)

T1