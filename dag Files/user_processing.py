from airflow.models import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import json
from datetime import datetime
from pandas import json_normalize

default_args = {
        'start_date':datetime(2020,1,1)
}

def _processing_user(ds, **kwargs): 
    ti = kwargs['ti'] 
    users = ti.xcom_pull(key="return_value",task_ids="extracting_user")
    if not len(users):
        raise ValueError('user is empty')
    
    users=json.loads(users)



    user=users['results'] 
    processed_user=json_normalize({ 
        'firstname':user[0]['name']['first'],
        'lastname':user[0]['name']['last'],
        'country':user[0]['location']['country'], 
        'username':user[0]['login']['username'],
        'password':user[0]['login']['password'], 
        'email':user[0]['email']
    })
    processed_user.to_csv('/tmp/processed_user.csv',index=None,header=False)



with DAG('user_processing',schedule_interval='@daily',
        default_args=default_args,catchup=False,) as dag:
   
    #define tasks/operators
    creating_table = SqliteOperator(
        task_id='creating_table',
        sqlite_conn_id='db_sqlite',
        sql='''
                create table if not exists users( 
                    firstname text not null,
                    lastname text not null,
                    country text not null,
                    username text not null,
                    password text not null,
                    email text not null primary key 
                  );
              '''

    )
    
    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='api/'
    )


    extracting_user=SimpleHttpOperator( 
        task_id='extracting_user',
        http_conn_id='user_api',
        endpoint='api/',
        method='GET',
        headers={"Content-Type": "application/json"}, 
        response_filter=lambda response:json.loads(json.dumps(response.text)),
        log_response=True
    )


    processing_user = PythonOperator(
        task_id = 'processing_user',
        python_callable=_processing_user
    )


    storing_user=BashOperator(
        task_id='storing_user',
        bash_command='echo -e ".separator ","\n.import /tmp/processed_user.csv users" |sqlite3 /opt/airflow/ersin.db'
    )


    creating_table >> is_api_available >>  extracting_user >> processing_user >> storing_user