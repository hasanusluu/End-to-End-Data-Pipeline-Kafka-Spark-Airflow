from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'daily_report_dag',
    default_args=default_args,
    description='A simple daily report DAG',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
) as dag:

    generate_report = DockerOperator(
        task_id='generate_report',
        image='apache/spark:3.5.0',
        container_name='spark_daily_report_task',
        api_version='auto',
        auto_remove=True,
        user='root',
        mount_tmp_dir=False,
        command='/opt/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 --master local[*] /opt/spark-apps/batch_daily_report.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='to-do-agent_default',
        mounts=[
            # Mount the spark-jobs directory from the host to the container
            {
                'Source': 'c:/Users/ADMIN/OneDrive/Desktop/To-Do-Agent/spark-jobs',
                'Target': '/opt/spark-apps',
                'Type': 'bind'
            }
        ]
    )

    generate_report
