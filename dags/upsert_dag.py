from airflow import DAG
from realtime_processor.db.upsert_to_main_table import upsert_to_main_table
try:
    from airflow.operators.python import PythonOperator
except ImportError:
    from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# Thêm thư mục realtime_processor/ vào PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))



default_args = {
    'owner': 'DiuNguyen',
    'start_date': datetime(2025, 7, 18),
    'catchup': False
}

with DAG("pharmaceutical_upsert_dag",
         schedule=None,
         default_args=default_args,
         description="Upsert data from staging to main table") as dag:

    upsert_task = PythonOperator(
        task_id="upsert_pharmaceutical_data",
        python_callable=upsert_to_main_table
    )

    upsert_task
