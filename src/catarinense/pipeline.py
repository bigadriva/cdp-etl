"""Este módulo contém uma função única para realizar todo o pipeline de ETL da
catarinense, desde baixar os dados e processá-los até fazer o upload e update
dos dados no banco."""

from typing import Callable, Dict

from src.catarinense.extract import extract
from src.catarinense.transform import transform
from src.catarinense.load import load


def pipeline(services_factories: Dict[str, Callable]):
    """Realiza todo o pipeline de ETL da catarinense.
    
    Args
        services_factories (dict) -- Os serviços necessários
    """
    print('Iniciando pipeline CATARINENSE')
    db_service_factory = services_factories['db']
    print('Iniciando EXTRACT CATARINENSE')
    # extract()
    print('Iniciando TRANSFORM CATARINENSE')
    entities = transform(services_factories)
    print(f'Created {sum(len(entities_list) for entities_list in entities)} entities')
    print('Iniciando LOAD CATARINENSE')
    load(entities, db_service_factory)
    # print(os.listdir('../data/catarinense'))
