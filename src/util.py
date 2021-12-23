from typing import Callable

from src.services.db import Connection

def schema_already_exists(create_connection: Callable[[], Connection], schema_name: str) -> bool:
    """Determina se já existe um schema no postgres com o nome passado.
    
    Args
        create_connection (Callable[[], Connection]) -- Uma função para criar o
            serviço de banco de dados. Retorna uma conexão com o postgres.
        schema_name (str) -- O nome do schema que se quer checar.

    Returns
        bool -- Se já existe ou não.
    """
    with create_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT schema_name FROM information_schema.schemata
            ''')
            schema_names = cur.fetchall()
            schema_names = [_schema_name[0] for _schema_name in schema_names]
    
    return schema_name in schema_names


def create_schema_in_db(create_connection: Callable[[], Connection], schema_name: str) -> None:
    """Cria um schema no banco com o nome passado.
    Args
        create_connection (Callable[[], Connection]) -- Uma função para criar o
            serviço de banco de dados. Retorna uma conexão com o postgres.
        schema_name (str) -- O nome do schema que se quer criar.

    Returns
        None.
    """
    with create_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f'CREATE SCHEMA {schema_name}')
