#Creacion de operador en airflow para la insercion de datos con postgres
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.postgres.hooks.postgres import PostgresHook
import json

class PostgresFileOperator(BaseOperator):
    
    @apply_defaults
    def __init__(self,
                 operation,
                 config={},
                 *args,
                 **kwargs):
        super(PostgresFileOperator, self).__init__(*args, **kwargs)
        self.operation = operation
        self.config = config
        self.postgres_hook = PostgresHook(postgres_conn_id='postgres_localhost')
        
    def execute(self, context):
        if self.operation == "write":
            self.writeInDb()
        elif self.operation == "read":
            self.readFromDb()
        
    def writeInDb(self):
        self.postgres_hook.bulk_load(self.config.get("table_name"), "/opt/airflow/data/file.csv")
        
    def readFromDb(self):
        conn = self.postgres_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute(self.config.get("query"))

        data = [doc for doc in cursor]
        print(data)
