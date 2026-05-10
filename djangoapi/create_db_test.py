"""
Crea la base de datos 'test_metatierrascol' para ejecutar los test automáticos.

Se debe ejecutar:

python manage.py test --keepdb

Si 'test_metatierrascol' ya existe la borra y luego la crea.

Para cargar los datos establece la variable de entorno:
    os.environ['MODE_TEST'] = 'True' 

Esto cambia el nombre de la bbdd en settings.py para que haga las migraciones y 
cree los esquemas, tablas y cargue los datos en la base de datos 'test_metatierrascol'.

Una vez ha terminado vuelve a poner:
    os.environ['MODE_TEST'] = 'False'

Para que settings.py vuelva a trabajar con la base de datos 'metatierrascol' 
"""

import os
import subprocess

from core.myLib.pgOperations import PgConnect, PgDatabases

con=PgConnect(
    database=os.getenv('POSTGRES_DB'),
    user= os.getenv('POSTGRES_USER'),
    password= os.getenv('POSTGRES_PASSWORD'),
    host= os.getenv('POSTGRES_HOST'),
    port= os.getenv('POSTGRES_PORT')
)

db=PgDatabases(con)

DATABASE_NAME = 'test_'+ os.getenv('POSTGRES_DB')
if db.databaseExists(databaseName=DATABASE_NAME):
    db.dropDatabase(DATABASE_NAME)

db.createDatabase(databaseName=DATABASE_NAME,addPostgisExtension=True,closeNewConnection=True)
con.disconnect()

#para que use la base de datos de test_metatierrascol en settings.py
os.environ['MODE_TEST'] = 'True'
try:
    # 3. Ahora que la BD existe y está vacía, ejecutamos tu script
    # Este script DEBE crear los esquemas (CREATE SCHEMA codelist...)
    print("--- Inicializando esquemas y datos base para la base de datos de test ---")
    subprocess.run(["sh", "./initdb.sh"], check=True)
    
except Exception as e:
    print(f"Error durante la inicialización: {e}")
    raise

#para que use la base de datos metatierrascol en settings.py
os.environ['MODE_TEST'] = 'False'
