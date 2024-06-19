# Proyecto Data Engineering 
## ETL de Mercado Libre

### Descripcion
Este proyecto de ingeniería de datos se baso en realizar el proceso de ETL(Extract, Transform, Load) de la Api de Mercado Libre, especificamente del el Producto Microondas.
En este proyecto hice enfasis en herramientas de orquestación como Airflow, para realizar las tareas de obtencion de datos, transformarlos y isertarlo en una base de datos PostgreSQL con el agregado de si en algun producto supera los 100.000 $ se enviará un correo hacia un destinatario indicando este triggers.

### Requisitos para el proyecto
.Python3
.Docker(Principal herramienta que contiene, Airflow, PostgreSQL. Podrá ver la configuración de mi docker-compose dónde tengo los servicios de Airflow y PostgreSQL)
.Gestor de base de datos(En este caso use Dbeaver)


