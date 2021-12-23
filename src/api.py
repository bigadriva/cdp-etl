# from typing import Optional

import os
from typing import Dict
from src.services.db import create_connection, create_engine
from src.util import create_schema_in_db, schema_already_exists
from fastapi import FastAPI

from src.catarinense.pipeline import pipeline as pipeline_catarinense

app = FastAPI() 


@app.get('/')
def read_root():
    return { 'Hello': 'World' }


@app.get('/pipeline')
def pipeline():
    try:
        services_factories = { 'db': create_connection }
        pipeline_catarinense(services_factories)
    except Exception as e:
        print(e)
        return {'status': 'deu ruim'}

    return {'status': 'deu bom'}


@app.post('/schema/{schema_name}')
def create_schema(schema_name: str) -> Dict[str, str]:
    """Cria um schema no banco de dados com o nome especificado.
    
    Comportamento
    ----------------------------------------------------------------------------
        Se já existir um schema com o mesmo nome, não será feito nada no banco e
        será retornado um objeto de resposta da seguinte maneira:
        {
            "status": "failed",
            "reason": "Schema name already in use."
        }

        Se não existir um schema com o nome especificado, será criado um com ele
        no banco.
            Se houver um erro de conexão com o banco, será retornado um objeto
            de resposta da seguinte maneira:
            {
                "status": "failed",
                "reason": "Connection failed."
            }

            Se houver um erro interno do postgres ao criar um schema, será
            retornado um objeto de resposta da seguinte maneira:
            {
                "status": "failed",
                "reason": "Postgres error."
            }

            Se o schema for criado com sucesso, será retornado um objeto de
            resposta da seguinte maneira:
            {
                "status": "success",
                "reason": "You are AWESOME!"
            }



    Assinatura
    ----------------------------------------------------------------------------

    Args
        schema_name (str) -- O nome do schema a ser criado.

    Returns
        Dict[str, str] -- A mensagem de resultado.
    """
    response = None

    if schema_already_exists(create_connection, schema_name):
        response = {
            "status": "failed",
            "reason": "Schema name already in use."
        }

    else:
        try:
            create_schema_in_db(create_connection, schema_name)
            response = {
                "status": "success",
                "reason": "You are AWESOME!"
            }
        except:
            response = {
                "status": "failed",
                "reason": "Postgres error."
            }

    return response    


@app.post('/tables')
def create_tables() -> Dict[str, str]:
    """Cria o schema cdp e as tabelas do CDP no schema cdp.

    As tabelas podem ser criadas executando o script SQL create_tables.

    Returns
        Dict[str, str] -- A mensagem de resposta.
    """
    response = None
    with create_connection() as conn:
        with conn.cursor() as cur:
            with open('src/sql/create_tables.sql', 'r') as sql_file:
                try:
                    cur.execute(sql_file.read())
                    response = {
                        "status": "success",
                        "reason": "You are AWESOME!"
                    }
                except:
                    response = {
                        "status": "failed",
                        "reason": "Postgres error."
                    }
    return response
