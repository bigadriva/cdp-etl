# from typing import Optional

import time
from src.data import create_catarinense_data
from src.upload import toPostgre
from src.services.db import create_connection
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

@app.get('/catarinense_data')
def catarinense_data():
    data = create_catarinense_data()
    toPostgre(data, 'catarinense_data')
