"""Este módulo conterá alguns serviços que poderão ser utilizados pelo app.

Entre os já implementados estão:
    - Criação de conexão com PostgreSQL;
"""

import os

import psycopg2

Connection = object

def create_connection():
    """Cria uma conexão com o PostgreSQL.
    
    Returns
        connection -- A conexão com o PostgreSQL gerada pelo pacote psycopg2.
    """
    dbname = os.getenv('POSTGRES_DBNAME')
    host = os.getenv('POSTGRES_HOST')
    user = os.getenv('POSTGRES_USER')
    passwd = os.getenv('POSTGRES_PASSWORD')

    return psycopg2.connect(dbname=dbname, user=user, password=passwd, host=host)
