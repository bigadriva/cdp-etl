"""Este módulo cuida do carregamento no banco de dados das entidades geradas."""

from typing import List, Callable
from src.models.base import BaseModel

from src.services.db import Connection

def load(entities: List[List[BaseModel]], db_service_factory: Callable[[], Connection]) -> None:
    """Carrega as entidades passadas no banco de dados.
    
    Args
        entities (List[dict]) -- As entidades a serem carregadas no banco.
        db_service_factory (Callable[[], Connection]) -- A factory para criação
            do serviço de banco de dados.
    """
    with db_service_factory() as conn:
        for entity_list in entities:
            for entity in entity_list:
                entity.upload_to_db(conn)
