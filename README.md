# airflow_on_openshift
Airflow on Openshift On All .yaml files


copy test dag python file into pod  
  * this command needs to run in folder contains "oc" client tool 
  * localpath contains "user_processing.py" file

.\oc rsync "localpath" airflow-worker-7df84f7cf-wzskc:/opt/airflow/dags/scheduler/


![okd-deployments](https://user-images.githubusercontent.com/6337752/169412691-754139fb-800f-4682-991d-afac46de83be.png)


![DAGs](https://user-images.githubusercontent.com/6337752/169412504-693f472a-0c71-48c3-9939-e3f10cc09a41.png)


![dag_graph](https://user-images.githubusercontent.com/6337752/169412528-71ad5ba3-7ab4-438f-b0e6-3a3482bef85f.png)


![dag_GANT](https://user-images.githubusercontent.com/6337752/169412537-b9dde9dc-783f-4659-b123-4d1901019cf2.png)


![flower](https://user-images.githubusercontent.com/6337752/169645015-5932a7c0-801f-4542-937a-3825abee27a5.png)
