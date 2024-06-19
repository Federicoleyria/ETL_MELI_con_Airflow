# Proyecto Data Engineering 
## ETL de Mercado Libre

### Descripcion
Este proyecto de ingeniería de datos se baso en realizar el proceso de ETL(Extract, Transform, Load) de la Api de Mercado Libre, especificamente del el Producto Microondas.
En este proyecto hice enfasis en herramientas de orquestación como Airflow, para realizar las tareas de obtencion de datos, transformarlos y isertarlo en una base de datos PostgreSQL con el agregado de si en algun producto supera los 100.000 $ se enviará un correo hacia un destinatario indicando este triggers.

### Requisitos para el proyecto
.Python3

.Docker(Principal herramienta que contiene, Airflow, PostgreSQL. Podrá ver la configuración de mi docker-compose dónde tengo los servicios de Airflow y PostgreSQL)

.Gestor de base de datos(En este caso use Dbeaver)

### Descripción del Pipeline
Este pipeline de ETL se compone de varias tareas definidas en un DAG de Airflow. A continuación se describe cada tarea:

Crear Tabla en PostgreSQL: Utiliza PostgresOperator para crear una tabla en la base de datos si no existe.

Consultar API de MercadoLibre: Utiliza BashOperator para ejecutar un script en Python que consulta la API de MercadoLibre y guarda los datos en un archivo CSV.

Insertar Datos en PostgreSQL: Utiliza un operador personalizado PostgresFileOperator para insertar los datos del archivo CSV en la tabla de PostgreSQL.

Leer Datos de PostgreSQL: Utiliza el mismo operador personalizado PostgresFileOperator para leer datos de la tabla de PostgreSQL.

Enviar Correo Electrónico: Utiliza PythonOperator para enviar un correo electrónico si se encuentran resultados específicos en la consulta a PostgreSQL.


### Problemas surgido durante el proyecto
 Creación Operador Personalizado para PostgreSQL
El operador PostgresFileOperator es un operador personalizado para manejar la inserción y lectura de datos desde un archivo CSV a PostgreSQL y viceversa. Este operador se debio crear ya que Airflow no tiene operadores de inserción en base de datos PostgreSQL con el operador PostgresOperator. Problema que se resolvio mendiante documentación y videos.


