"""Este módulo cuida do carregamento no banco de dados das entidades geradas."""

from typing import List, Callable
from src.models.base import BaseModel

from src.services.db import Connection

def load(entities_generator: List[BaseModel], db_service_factory: Callable[[], Connection]) -> None:
    """Carrega as entidades passadas no banco de dados.
    
    Args
        entities_generator (List[dict]) -- As entidades a serem carregadas no banco.
        db_service_factory (Callable[[], Connection]) -- A factory para criação
            do serviço de banco de dados.
    """
    for entities in entities_generator:
        with db_service_factory() as conn:
            for entity in entities:
                entity.upload_to_db(conn)
