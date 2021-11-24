"""Este módulo contém funções para criar instâncias dos modelos definidos e
fazer o upload dos dados para o banco de dados utilizado."""

import pandas as pd

from typing import Callable, Dict, List

from src.services.util import Service

from src.models.base import BaseModel
from src.models.entities.client import Client
from src.models.entities.company import Company
from src.models.entities.salesperson import Salesperson
from src.models.entities.acting_region import ActingRegion
from src.models.entities.product import Product
from src.models.relationships.buys_from import BuysFrom
from src.models.relationships.sells_to import SellsTo
from src.models.relationships.sells import Sells
from src.models.relationships.acts_in import ActsIn

from src.services.enrich import enrich


def transform(services_factories: Dict[str, Callable[[], Service]]) -> List[List[BaseModel]]:
    """Realiza a etapa de transformação dos dados.

    Returns
        List[dict].
    """
    company_list = []
    product_list = []
    acting_region_list = []
    salesperson_list = []
    client_list = []
    buys_from_list = []
    sells_to_list = []
    sells_list = []
    acts_in_list = []


    path_prefix = 'data/catarinense'

    df_dados = pd.read_csv(f'{path_prefix}/dados_driva.csv', delimiter=';', dtype=str)
    df_vend = pd.read_csv(f'{path_prefix}/vend_driva.csv', delimiter=';', dtype=str)
    df_prod = pd.read_csv(f'{path_prefix}/prod_driva.csv', delimiter=';', dtype=str)

    df = pd.merge(df_dados, df_vend,
                        how="left", left_on="VEND_NF", right_on="VEND_CLI")
    df = pd.merge(df, df_prod,
                        how="left", left_on="COD", right_on="CODIGO")
    df = df.rename(columns={
        "CNPJ": "cnpj",
        "AREA_CLI": "area_client",
        "NOME_VEND_CLI": "consultor",
        "RAZAO SOCIAL": "razao_social",
        "DATA": "data",
        "QTD_FAT": "qtd_s_refat",
        "QTD_LOG_FAT": "qtd_ol",
        "VAL_FAT": "valor_fat",
        'VAL_LOG_FAT': 'valor_ol',
        "PRODUTO": "produto",
        'CODIGO': 'codigo',
        'FAMILIA': 'familia'
    })

    df = df[df['cnpj'] != '00000000000000']

    df = df.iloc[:min(df.shape[0], 2_000_000), :]

    df = enrich(df)

    out_prefix = 'out'
    df.to_csv(f'{out_prefix}/all.csv', sep=';')

    if df is not None:
        # Podem existir erros no dataframe ou preenchimentos que não fazem sentido.
        # Por exemplo, pode existir um registro com CNPJ 00000000000000, o que não
        # nos ajuda em nada no preenchimento da base. Para esses casos, a etapa de
        # enriquecimento não retornará endereço, nem bairro, nem municipio. Então,
        # um dropna deve se livrar de boa parte dos casos em que os dados não fazem
        # sentido.
        df = df.dropna(subset=['municipio'])
        num_failed = 0

        for row in df.to_dict('records'):
            # ----------------------------------------------------------------------
            # Transformando entidades

            # Clientes da driva.
            company = transform_companies(row)
            if company is not None:
                company_list.append(company)

            product = transform_products(row)
            if product is not None:
                product_list.append(product)

            acting_region = transform_acting_regions(row)
            if acting_region is not None:
                acting_region_list.append(acting_region)

            salesperson = transform_salespersons(row)
            if salesperson is not None:
                salesperson_list.append(salesperson)

            # Clientes das empresas clientes da driva.
            client = transform_clients(row)
            if client is not None:
                client_list.append(client)


            if company is not None:
                salesperson.references_company(company)
    
            if acting_region is not None:
                client.references_acting_region(acting_region)

            # ----------------------------------------------------------------------
            # Transformando relacionamentos

            if company is not None and client is not None:
                buys_from = BuysFrom()
                buys_from.references_company(company)
                buys_from.references_client(client)
                buys_from_list.append(buys_from)

            if client is not None and salesperson is not None:
                sells_to = SellsTo()
                sells_to.references_client(client)
                sells_to.references_salesperson(salesperson)
                sells_to_list.append(sells_to)

            if salesperson is not None and product is not None:
                sells = transform_sells(row)
                sells.references_salesperson(salesperson)
                sells.references_product(product)
                sells_list.append(sells)

            if salesperson is not None and acting_region is not None:
                acts_in = ActsIn()
                acts_in.references_salesperson(salesperson)
                acts_in.references_acting_region(acting_region)
                acts_in_list.append(acts_in)

                

        print(f'Ocorreram erros em {num_failed} dos {len(df)} registros.')


    entities = [
        company_list,
        product_list,
        acting_region_list,
        salesperson_list,
        client_list,
        buys_from_list,
        sells_to_list,
        sells_list,
        acts_in_list
    ]

    return entities


def transform_companies(row: dict) -> Company:
    """Realiza a etapa de transformação dos dados de clientes da driva.

    Args
        row (dict) -- O registro a ser transformado.

    Returns
        Company -- A classe representante da Catarinense.
    """
    catarinense = Company()
    catarinense.cnpj = '84684620000187'
    catarinense.name = 'Catarinense Pharma'
    return catarinense


def transform_products(row: dict) -> Product:
    """Realiza a etapa de transformação dos dados de produtos.

    Args
        row (dict) -- O registro a ser transformado.

    Returns
        Product -- A lista de produtos contidos na base lida.
    """
    product = Product()
    product.name = row['produto']
    product.internal_id = row['codigo']
    product.type = row['familia']

    if product.internal_id == '':
        product = None

    return product



def transform_acting_regions(row: dict) -> ActingRegion:
    """Realiza a etapa de transformação dos dados de regiões de atuação.

    Args
        row (dict) -- O registro a ser transformado.

    Returns
        ActingRegion -- A lista de regiões de atuação contidas na base lida.
    """
    acting_region = ActingRegion()
    acting_region.city = row['municipio']
    acting_region.neighborhood = row['bairro']
    acting_region.address = row['endereco']

    if acting_region.city == '' \
            or acting_region.address == '':
        acting_region = None

    return acting_region


def transform_salespersons(row: dict) -> Salesperson:
    """Realiza a etapa de transformação dos dados de vendedores.

    Args
        row (dict) -- O registro a ser transformado.

    Returns
        Salesperson -- A lista de vendedores contidas na base lida.
    """
    salesperson = Salesperson()
    name_cli = row['consultor']
    name_cli = name_cli.split('-')
    if name_cli:
        salesperson.name = name_cli[1].strip()
        salesperson.internal_id = name_cli[0].strip()
        if salesperson.name == '' or salesperson.name is None:
            raise Exception('Parou')

    if salesperson.name == '' or salesperson.internal_id == '':
        salesperson = None

    return salesperson


def transform_clients(row: dict) -> Client:
    """Realiza a etapa de transformação dos dados de clientes.

    Args
        row (dict) -- O registro a ser transformado.

    Returns
        Client -- A lista de clientes contidos na base lida.
                        Clientes dos clientes da driva.
    """
    client = Client()
    client.cnpj = row['cnpj']
    client.name = row['razao_social']

    if client.cnpj == '':
        client = None
    
    return client


def transform_sells(row: dict) -> Sells:
    """Realiza a etapa de transformação dos dados de vendas.

    Args
        row (dict) -- O registro a ser transformado.

    Returns
        Sells -- O registro da venda realizada.
    """
    sell = Sells()
    sell.date = row['data']
    
    return sell
