#!/bin/bash
pip install -r /opt/airflow/requirements.txt
airflow db upgrade
airflow users create \
    --username admin \
    --password admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com
exec airflow webserver