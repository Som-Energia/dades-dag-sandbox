from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from util_tasks.t_branch_pull_ssh import build_branch_pull_ssh_task
from util_tasks.t_git_clone_ssh import build_git_clone_ssh_task
from util_tasks.t_check_repo import build_check_repo_task
from util_tasks.t_update_docker_image import build_update_image_task
from docker.types import Mount, DriverConfig
from datetime import datetime, timedelta
from airflow.models import Variable
from urllib.parse import urlparse
from pathlib import Path

my_email = Variable.get("fail_email")
addr = Variable.get("repo_server_url")

args= {
  'email': my_email,
  'email_on_failure': False,
  'email_on_retry': False,
  'retries': 0,
  'retry_delay': timedelta(minutes=5),
}

nfs_config = {
    'type': 'nfs',
    'o': f'addr={addr},nfsvers=4',
    'device': ':/opt/airflow/repos'
}

driver_config = DriverConfig(name='local', options=nfs_config)
mount_nfs = Mount(source="local", target="/repos", type="volume", driver_config=driver_config)

with DAG(dag_id='dades_sandbox_fal_dag', start_date=datetime(2020,3,20), schedule_interval='@hourly', catchup=False, tags=["Sandbox"], default_args=args) as dag:

    repo_name = 'dades-dag-sandbox'

    task_check_repo = build_check_repo_task(dag=dag, repo_name=repo_name)
    task_git_clone = build_git_clone_ssh_task(dag=dag, repo_name=repo_name)
    task_branch_pull_ssh = build_branch_pull_ssh_task(dag=dag, task_name='fal_task', repo_name=repo_name)
    task_update_image = build_update_image_task(dag=dag, repo_name=repo_name)

    # fragile dbapi to user-password combination

    dbapi = '{{ var.value.puppis_sandbox_db }}'
    dbapi = 'postgresql://somuser:ees%3Fe@puppis.somenergia.lan:5432/sandbox'
    parsed_dbapi = urlparse(dbapi)
    print(parsed_dbapi)
    assert parsed_dbapi

    if len(parsed_dbapi.netloc.split('@')) != 2:
        raise Exception(parsed_dbapi.netloc)

    userinfo,hostinfo = parsed_dbapi.netloc.split('@')

    db_host, db_port = hostinfo.split(':')
    db_user, db_password = userinfo.split(':')
    db_name = Path(parsed_dbapi.path).name

    assert db_user
    assert db_password
    assert db_host
    assert db_port
    assert db_name

    fal_task = DockerOperator(
        api_version='auto',
        task_id='fal_task',
        docker_conn_id='somenergia_registry',
        image='{}/{}-requirements:latest'.format('{{ conn.somenergia_registry.host }}',repo_name),
        working_dir=f'/repos/{repo_name}/dbt_dades_sandbox',
        command='DBUSER="{}" DBPASSWORD="{}" DBHOST="{}" DBPORT="{}" DBNAME="{}" fal flow run --profile-dir config'.format(db_user, db_password, db_host, db_port, db_name),
        docker_url=Variable.get("generic_moll_url"),
        mounts=[mount_nfs],
        mount_tmp_dir=False,
        auto_remove=True,
        retrieve_output=True,
        trigger_rule='none_failed',
    )

    task_check_repo >> task_git_clone
    task_check_repo >> task_branch_pull_ssh
    task_git_clone >> task_update_image
    task_branch_pull_ssh >> task_update_image
    task_branch_pull_ssh >> fal_task
    task_update_image >> fal_task