"""Este módulo cuida do carregamento no banco de dados das entidades geradas."""

from typing import List, Callable

import pandas as pd
from src.models.entities.client import Client
from src.models.base import BaseModel

from src.services.db import Connection

def load(entities_generator: List[List[BaseModel]], db_service_factory: Callable[[], Connection]) -> None:
    """Carrega as entidades passadas no banco de dados.
    
    Args
        entities_generator (List[dict]) -- As entidades a serem carregadas no banco.
        db_service_factory (Callable[[], Connection]) -- A factory para criação
            do serviço de banco de dados.
    """
    num_clients = 0
    for entities in entities_generator:
        with db_service_factory() as conn:
            with conn.cursor() as cur:
                for entity in entities:
                    print(f'Enviando {entity.table_name}')
                    print(entity.to_dict())
                    print('\n')
                    entity.upload_to_db(cur)
    print(f'Foram carregados {num_clients} clientes')
