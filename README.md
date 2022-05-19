# airflow_on_openshift
Airflow on Openshift On All .yaml files


copy test dag python file into pod  
  * this command needs to run in folder contains "oc" client tool 
  * localpath contains "user_processing.py" file

.\oc rsync "localpath" airflow-worker-7df84f7cf-wzskc:/opt/airflow/dags/scheduler/