import os
from pgOperations import pgOperations as pg

def getConnection()->pg.PgConnection:
    NAME=os.getenv('POSTGRES_DB')
    USER=os.getenv('POSTGRES_USER')
    PASSWORD=os.getenv('POSTGRES_PASSWORD')
    HOST=os.getenv('POSTGRES_HOST')
    PORT=os.getenv('POSTGRES_PORT')
    conn=pg.PgConnect(NAME,USER,PASSWORD,HOST,PORT)
    return conn

def getPg(connection=None)->pg.PgOperations:
    if not connection:
        connection=getConnection()
    return pg.PgOperations(connection)
    