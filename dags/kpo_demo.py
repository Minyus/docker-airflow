from airflow import DAG

from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 6, 25),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=60),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2021, 1, 1),
}

dag = DAG(
    "kubernetes_pod_demo",
    default_args=default_args,
    schedule_interval=timedelta(seconds=60),
    catchup=False,
)

'''
1. Set up Kubernetes cluster.
   If you use kind, run "kind create cluster --config kind-config.yml"
   kind-config.yml file should be like:
"""
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
networking:
  apiServerAddress: "0.0.0.0" # Note: This setup is easy but not secure.
"""
2. Run "kubectl config view --minify --raw" and save as kubeconfig.yml
3. Modify the clusters.cluster.server.
   The IP address is the one of the Kubernetes API instead of "0.0.0.0"
   (If you use kind, run "docker network inspect kind" and find "kind-control-plane")
   The port is usually 6443.
'''

t1 = KubernetesPodOperator(
    dag=dag,
    config_file="/usr/local/airflow/dags/kubeconfig.yml",
    in_cluster=False,
    xcom_push=False,
    task_id="kpo_demo_task",
    name="kpo_demo",
    cmds=["echo"],
    namespace="default",
    image="gcr.io/gcp-runtimes/ubuntu_18_0_4",
)
