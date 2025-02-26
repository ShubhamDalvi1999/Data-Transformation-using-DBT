from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable
from airflow.models.baseoperator import chain
from airflow.decorators import dag, task, task_group
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

#pendulum required for timezonde aware dags
import pendulum
from sodapy import Socrata

import pandas as pd
import threading
import time
from datetime import datetime

dbt_project_dir = Variable.get("dbt_project_dir")

@dag(
    # every week on wednesday?
    # every Friday at 3:30 p.m. Eastern time.

    # Time zone aware DAGs that use cron schedules respect daylight savings time.
    # For example, a DAG with a start date in the US/Eastern time zone
    # with a schedule of 0 0 * * * will run daily at 04:00 UTC during daylight savings time
    # and at 05:00 otherwise.

    dag_id='ingest_cftc_report',
    schedule_interval = '31 15 * * 5', 

    start_date=pendulum.datetime(2024, 1, 1, tz="US/Eastern"), 
    
    catchup=False, 
    
    tags=["cftc"],
    
    max_active_tasks=1

    )

def ingest_cftc_data():
    
    @task()
    def start():
        start_task = EmptyOperator(
        task_id="start"
        )
        
    @task(
        task_id="cftc_ingest",
        retries=3,
        retry_delay=pendulum.duration(minutes=5),
        retry_exponential_backoff=True,
        max_retry_delay=pendulum.duration(minutes=15)
    )   
    def cftc_ingest(**context):
        postgres_hook = PostgresHook(postgres_conn_id="db")
        commodity_code_dict = {'Wheat': '001602',
                                'Corn': '002602',
                                'Oilseed, Soybean': '005602',
                                'soybean Meal': '026603',
                                'Soybean Oil':'007601'}
        
        # Configure Socrata client with timeout
        client = Socrata("publicreporting.cftc.gov", None, timeout=60)

        try:
            # MAIN SOURCE URL : https://publicreporting.cftc.gov/stories/s/Commitments-of-Traders/r4w3-av2u/?utm_source=chatgpt.com
            # SOURCE URL : https://publicreporting.cftc.gov/stories/s/Disaggregated-Combined/gr4m-cvuh/
            # API URL: https://dev.socrata.com/foundry/publicreporting.cftc.gov/kh3c-gbw2

            results = client.get("jun7-fc8e", select="\
                        report_date_as_yyyy_mm_dd, \
                        contract_market_name, \
                        cftc_market_code, \
                        cftc_commodity_code, \
                        commodity_name, \
                        pct_of_oi_comm_long_all,\
                        pct_of_oi_comm_short_all,\
                        pct_of_oi_noncomm_long_all,\
                        pct_of_oi_noncomm_short_all", 
                         where="(cftc_contract_market_code == '001602' OR \
                                cftc_contract_market_code == '002602' OR \
                                cftc_contract_market_code == '005602' OR \
                                cftc_contract_market_code == '026603' OR \
                                cftc_contract_market_code == '007601' ) \
                                 AND \
                                (report_date_as_yyyy_mm_dd >= '1994-01-01T00:00:00.000')",
                         order="report_date_as_yyyy_mm_dd",
                         limit=50000)
            
            df = pd.DataFrame.from_records(results)
            df['report_date_as_yyyy_mm_dd'] = pd.to_datetime(df['report_date_as_yyyy_mm_dd'])

            df["pct_of_oi_comm_long_all"] = df["pct_of_oi_comm_long_all"].astype(float)
            df["pct_of_oi_comm_short_all"] = df["pct_of_oi_comm_short_all"].astype(float)
            df["pct_of_oi_noncomm_long_all"] = df["pct_of_oi_noncomm_long_all"].astype(float)
            df["pct_of_oi_noncomm_short_all"] = df["pct_of_oi_noncomm_short_all"].astype(float)

            df.to_sql('05_COT_Legacy_Combined_Report', postgres_hook.get_sqlalchemy_engine(), schema='raw',if_exists='replace', index=False)
            return "Data ingested successfully"
        except Exception as e:
            print(f"Error during data ingestion: {str(e)}")
            raise
        finally:
            client.close()

    run_dbt_debug = DockerOperator(
        task_id='run_dbt_debug',
        image='docker_airflow_postgres-main-dbt',
        command=["debug"],
        container_name='dsec-dbt',
        api_version='auto',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='docker_airflow_postgres-main_default',
        mounts = [Mount(
            source=dbt_project_dir, target="/dsec_dbt", type="bind")],
        mount_tmp_dir=False,
        working_dir="/dsec_dbt",
        environment={ 
            'DB_HOST': 'docker_airflow_postgres-main-postgres-1',
            'DB_USER': '{{var.value.db_user}}',
            'DB_ADMIN_PASSWORD': '{{var.value.db_admin_password}}',
            'DB_PORT': '{{var.value.db_port}}',
            'DB_NAME': '{{var.value.db_name}}',
            'DB_SCHEMA': '{{var.value.db_schema}}'
        },
        retries=2,
        retry_delay=pendulum.duration(minutes=5)
    )

    run_dbt_deps = DockerOperator(
        task_id='run_dbt_deps',
        image='docker_airflow_postgres-main-dbt',
        command=["deps"],
        container_name='dsec-dbt',
        api_version='auto',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='docker_airflow_postgres-main_default',
        mounts = [Mount(
            source=dbt_project_dir, target="/dsec_dbt", type="bind")],
        mount_tmp_dir=False,
        working_dir="/dsec_dbt",
        environment={ 
            'DB_HOST': 'docker_airflow_postgres-main-postgres-1',
            'DB_USER': '{{var.value.db_user}}',
            'DB_ADMIN_PASSWORD': '{{var.value.db_admin_password}}',
            'DB_PORT': '{{var.value.db_port}}',
            'DB_NAME': '{{var.value.db_name}}',
            'DB_SCHEMA': '{{var.value.db_schema}}'
        },
        retries=2,
        retry_delay=pendulum.duration(minutes=5)
    )

    run_dbt_model = DockerOperator(
        task_id='run_dbt_model',
        image='docker_airflow_postgres-main-dbt',
        command=["run", "--models", "01_Refined_COT_Report"],
        container_name='dsec-dbt',
        api_version='auto',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='docker_airflow_postgres-main_default',
        mounts = [Mount(
            source=dbt_project_dir, target="/dsec_dbt", type="bind")],
        mount_tmp_dir=False,
        working_dir="/dsec_dbt",
        environment={ 
            'DB_HOST': 'docker_airflow_postgres-main-postgres-1',
            'DB_USER': '{{var.value.db_user}}',
            'DB_ADMIN_PASSWORD': '{{var.value.db_admin_password}}',
            'DB_PORT': '{{var.value.db_port}}',
            'DB_NAME': '{{var.value.db_name}}',
            'DB_SCHEMA': '{{var.value.db_schema}}'
        },
        retries=2,
        retry_delay=pendulum.duration(minutes=5)
    )

    run_dbt_test = DockerOperator(
        task_id='run_dbt_test',
        image='docker_airflow_postgres-main-dbt',
        command=["test", "--select", "01_Refined_COT_Report"],
        container_name='dsec-dbt',
        api_version='auto',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        
        # network_mode is used to connect the dbt container to the airflow container
        network_mode='docker_airflow_postgres-main_default',
        mounts = [Mount(
            source=dbt_project_dir, target="/dsec_dbt", type="bind")],
        mount_tmp_dir=False,
        working_dir="/dsec_dbt",
        environment={ 
            'DB_HOST': 'docker_airflow_postgres-main-postgres-1',
            'DB_USER': '{{var.value.db_user}}',
            'DB_ADMIN_PASSWORD': '{{var.value.db_admin_password}}',
            'DB_PORT': '{{var.value.db_port}}',
            'DB_NAME': '{{var.value.db_name}}',
            'DB_SCHEMA': '{{var.value.db_schema}}'
        },
        retries=2,
        retry_delay=pendulum.duration(minutes=5)
    )
        
    @task(task_id="end")
    def end():
        return "DAG completed successfully"
    
    # Set up task dependencies
    start_op = start()
    ingest_op = cftc_ingest()
    end_op = end()
    
    # Define the task chain
    start_op >> ingest_op >> run_dbt_debug >> run_dbt_deps >> run_dbt_model >> run_dbt_test >> end_op

dag = ingest_cftc_data()