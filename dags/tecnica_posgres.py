from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.email_operator import EmailOperator  # Importa EmailOperator
from datetime import datetime, timedelta
from operators.PostgresFileOperator import PostgresFileOperator

# Define los argumentos por defecto para el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define la función para enviar correo electrónico
def send_email_if_results_exist():
    from airflow.providers.postgres.hooks.postgres import PostgresHook

    postgres_hook = PostgresHook(postgres_conn_id='postgres_localhost')
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()
    query = "SELECT * FROM tecnica_ml WHERE cast(price as decimal) > 100000"
    cursor.execute(query)
    data = cursor.fetchall()

    if data:
        subject = "Resultados de consulta en PostgreSQL"
        body = f"Se encontraron resultados en la consulta:\n{data}"
        email_operator = EmailOperator(
            task_id='send_email_task',
            to='tu_correo@dominio.com',
            subject=subject,
            html_content=body
        )
        email_operator.execute(context=None)  # Ejecuta el envío del correo electrónico

# Define el DAG
with DAG(
    dag_id="tecnica_postgres",
    default_args=default_args,
    start_date=datetime(2024, 6, 18),
    schedule_interval=None,
) as dag:
    
    # Define la tarea PostgresOperator para crear la tabla
    task_1 = PostgresOperator(
        task_id="Crear_tabla",
        postgres_conn_id="postgres_localhost",
        sql='''
        CREATE TABLE IF NOT EXISTS tecnica_ml (
            id VARCHAR(255),
            title VARCHAR(255),
            price VARCHAR(255),
            thumbnail VARCHAR(255),
            created_date VARCHAR(50),
            PRIMARY KEY (id, created_date)
        );
        '''
    )
    
    # Define la tarea BashOperator para consultar la API y crear el CSV
    task_2 = BashOperator(
        task_id="Consultar_API",
        bash_command="python /opt/airflow/data/tmp/consult_api.py"  # Revisa el comando bash aquí
    )
    
    # Define la tarea PostgresFileOperator para insertar datos desde el CSV a PostgreSQL
    task_3 = PostgresFileOperator(
        task_id='Insertar_Datos',
        operation='write',
        config={"table_name": "tecnica_ml"} 
    )

    # Define la tarea PostgresFileOperator para leer datos desde PostgreSQL
    task_4 = PostgresFileOperator(
        task_id='Leer_Datos',
        operation='read',
        config={"query": "SELECT * FROM tecnica_ml WHERE cast(price as decimal) > 100000"} 
    )
    
    # Define la tarea PythonOperator para enviar correo electrónico si hay resultados en la consulta
    send_email_task = PythonOperator(
        task_id='enviar_email_si_resultados',
        python_callable=send_email_if_results_exist
    )
    
    # Define la secuencia de las tareas
    task_1 >> task_2 >> task_3 >> task_4 >> send_email_task
