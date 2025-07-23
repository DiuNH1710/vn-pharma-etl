from datetime import datetime
from airflow import DAG
from pipelines.dvc_pipeline import extract_dvc_data
try:
    from airflow.operators.python import PythonOperator
except ImportError:
    from airflow.providers.standard.operators.python import PythonOperator

import os
import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, '/opt/airflow')


# write_dvc_data, transform_dvc_data

default_args = {
    'owner': 'DiuNguyen',
    'start_date': datetime(2025, 7, 18)
}

dag = DAG('dvc_flow',
          default_args=default_args,
          schedule=None,
          catchup=False)

extract_data_from_DVC = PythonOperator(
    task_id='extract_data_from_DVC',
    provide_context=True,
    python_callable=extract_dvc_data,
    dag=dag
)

