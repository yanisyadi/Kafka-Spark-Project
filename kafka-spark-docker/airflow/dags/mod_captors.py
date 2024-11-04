import os
import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
import shutil

from airflow.utils.dates import days_ago


def copy_file(src_filename):
    src_path = f'/opt/airflow/captors/{src_filename}'
    dst_dir = '/opt/airflow/captors_data'
    dst_path = f'{dst_dir}/{src_filename}'

    print("Fetching data from captors")
    try:
        shutil.copyfile(src_path, dst_path)
        print("Successfully fetched captors data")
    except Exception as e:
        print(f'Error copying {src_path} to {dst_path}: {e}')

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

# DAG creation
dag = DAG(dag_id='captors_dag', default_args=default_args, schedule_interval=None)

files = ['1.json', '2.json', '3.json', '4.json']
tasks = []

with dag:
    for i, file in enumerate(files):
        task = PythonOperator(task_id=f'run_task{i+1}', python_callable=copy_file, op_kwargs={'src_filename': file})
        tasks.append(task)

    for index, task in enumerate(tasks):
        if index < len(files) - 1:
            tasks[index] >> tasks[index + 1]