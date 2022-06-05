# Airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.hooks.base_hook import BaseHook
from airflow.providers.postgres.operators.postgres import PostgresOperator

# Libs
import os, sys
from datetime import datetime, date, timedelta
from dateutil.relativedelta import *

# Dependencies
from dependencies.scripts import getIncrementalStrategy, readFile

default_args = {
    'owner': 'Emerge IT',
    'depends_on_past': False,
    'retries': 0,
    'email_on_failure': False,
    'email_on_retry': False,
}

with DAG('dag-incremental', 
        start_date=datetime(2022, 5, 30),
        max_active_runs=10,
        schedule_interval='*/5 * * * *',
        default_args=default_args,
        tags=["POSTGRES", "INCREMENTAL"],
        catchup=False,
        params={'full': "False"},
        is_paused_upon_creation=False
    ) as dag:


    init = DummyOperator(task_id="init")
    task_date = BashOperator(
        task_id="task_date", 
        bash_command=f"echo '{getIncrementalStrategy()}'", 
        retries=3
    )

    task_incremental = PostgresOperator(
        task_id="task_incremental",
        postgres_conn_id="postgres_default",
        sql=readFile(path='/app/airflow/dags/queries/raw_tb_radar.sql').replace(
            '${DATE}', 
            getIncrementalStrategy()
        )
    )

    final = DummyOperator(task_id="final")

init >> task_date >> task_incremental >> final