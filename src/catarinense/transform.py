"""Este módulo contém funções para criar instâncias dos modelos definidos e
fazer o upload dos dados para o banco de dados utilizado."""

import os
import pandas as pd

from typing import List

from src.models.util import process_currency_values
from src.models.base import BaseModel
from src.models.entities.client import Client
from src.models.entities.company import Company
from src.models.entities.salesperson import Salesperson
from src.models.entities.acting_region import ActingRegion
from src.models.entities.product import Product
from src.models.entities.sale import Sale
from src.models.entities.characteristics import Characteristics
from src.models.relationships.buys_from import BuysFrom
from src.models.relationships.sells_to import SellsTo
from src.models.relationships.acts_in import ActsIn

from src.services.enrich import enrich


def transform() -> List[BaseModel]:
    """Realiza a etapa de transformação dos dados.

    Returns
        List[dict].
    """
    path_prefix = 'data/catarinense'

    df_dados = pd.read_csv(f'{path_prefix}/dados_driva.csv', delimiter=';', dtype=str)
    df_vend = pd.read_csv(f'{path_prefix}/vend_driva.csv', delimiter=';', dtype=str)
    df_prod = pd.read_csv(f'{path_prefix}/prod_driva.csv', delimiter=';', dtype=str)
    df_close_up = pd.read_csv(f'{path_prefix}/close_up.csv', dtype=str)
    cols = ['CNPJ_PDV']
    cols.extend([col for col in df_close_up.columns if 'CAT' in col])
    df_close_up = df_close_up[cols]
    df_close_up['CNPJ_PDV'] = df_close_up['CNPJ_PDV'].str.zfill(14)
    df_close_up = df_close_up.rename(columns={'CNPJ_PDV': 'CNPJ'})


    df = df_dados.join(df_vend.set_index('VEND_CLI'), how="left", on="VEND_NF")
    df = df.join(df_prod.set_index('CODIGO'), how="left", on="COD")
    df = df.join(df_close_up.set_index('CNPJ'), how='outer', on='CNPJ')
    df = df.rename(columns={
        "AREA_CLI": "area_client",
        'CAT MERC DE XAROPE': 'cat_xarope',
        'CAT MERC DE DIGES LIQUIDOS': 'cat_diges_liquidos',
        'CAT MERC DE DIGES FLACONETES': 'cat_diges_flaconetes',
        'CAT MERC DE POLIVITAMINICOS': 'cat_polivitaminicos',
        'CAT MERC DE FITOVITAL': 'cat_fitovital',
        "CNPJ": "cnpj",
        'COD': 'codigo',
        "DATA": "data",
        'FAMILIA': 'familia',
        "NOME_VEND_CLI": "consultor",
        'NR_PEDIDO': 'numero_pedido',
        'QTD_FAT': 'qtd_fat',
        'QTD_LOG_FAT': 'qtd_log_fat',
        "PRODUTO": "produto",
        "RAZAO SOCIAL": "razao_social",
        'VAL_FAT': 'valor_fat',
        'VAL_LOG_FAT': 'valor_log_fat'
    })

    df = df[df['cnpj'] != '00000000000000']


    df = enrich(df)

    out_prefix = 'out'
    if not os.path.exists(out_prefix):
        os.mkdir(out_prefix)
    df.to_csv(f'{out_prefix}/all.csv', sep=';')
    df = df.fillna('')

    if df is not None:
        # Podem existir erros no dataframe ou preenchimentos que não fazem sentido.
        # Por exemplo, pode existir um registro com CNPJ 00000000000000, o que não
        # nos ajuda em nada no preenchimento da base. Para esses casos, a etapa de
        # enriquecimento não retornará endereço, nem bairro, nem municipio. Então,
        # um dropna deve se livrar de boa parte dos casos em que os dados não fazem
        # sentido.
        num_failed = 0

        for row in df.to_dict('records'):
            try:
                entities = []
                # ----------------------------------------------------------------------
                # Transformando entidades

                # Clientes da driva.
                company = transform_companies(row)
                if company is not None:
                    entities.append(company)
                print('Company')

                product = transform_products(row)
                if product is not None:
                    entities.append(product)
                print('Product')

                acting_region = transform_acting_regions(row)
                if acting_region is not None:
                    entities.append(acting_region)
                print('Acting Region')

                salesperson = transform_salespersons(row)
                if salesperson is not None:
                    entities.append(salesperson)
                print('Salesperson')

                # Clientes das empresas clientes da driva.
                client = transform_clients(row)
                if client is not None:
                    entities.append(client)
                print('Client')

                sale = transform_sale(row)
                if sale is not None:
                    entities.append(sale)
                print('Sale')

                characteristics = transform_characteristics(row)
                if characteristics is not None:
                    entities.append(characteristics)
                print('Characteristics')

                if salesperson is not None and company is not None:
                    salesperson.references_company(company)
                elif salesperson in entities:
                    entities.remove(salesperson)

                if client is not None and acting_region is not None:
                    client.references_acting_region(acting_region)
                elif client in entities:
                    entities.remove(client)
                    print('Removed client', client.to_dict())
                    client = None

                if sale is not None and client is not None:
                    sale.references_client(client)
                elif sale in entities:
                    entities.remove(sale)
                    print('Removed sale', sale.to_dict())
                    sale = None

                if sale is not None and product is not None:
                    sale.references_product(product)
                elif sale in entities:
                    entities.remove(sale)
                    print('Removed sale', sale.to_dict())
                    sale = None

                if sale is not None and salesperson is not None:
                    sale.references_salesperson(salesperson)
                elif sale in entities:
                    entities.remove(sale)
                    print('Removed sale', sale.to_dict())
                    sale = None

                # ----------------------------------------------------------------------
                # Transformando relacionamentos

                if company is not None and client is not None:
                    buys_from = BuysFrom()
                    buys_from.references_company(company)
                    buys_from.references_client(client)
                    entities.append(buys_from)

                if client is not None and salesperson is not None:
                    sells_to = SellsTo()
                    sells_to.references_client(client)
                    sells_to.references_salesperson(salesperson)
                    entities.append(sells_to)

                if salesperson is not None and acting_region is not None:
                    acts_in = ActsIn()
                    acts_in.references_salesperson(salesperson)
                    acts_in.references_acting_region(acting_region)
                    entities.append(acts_in)

            except Exception as e:
                print(e)
                print(company)
                print(product)
                print(acting_region)
                print(salesperson)
                print(client)
                print(sale)

            print('Yield')
            yield entities

        print(f'Ocorreram erros em {num_failed} dos {len(df)} registros.')


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
    product.name = row['produto'] if 'produto' in row else ''
    product.internal_id = row['codigo'] if 'codigo' in row else ''
    product.type = row['familia'] if 'familia' in row else ''

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
    acting_region.city = row['municipio'] if 'municipio' in row else ''
    acting_region.neighborhood = row['bairro'] if 'bairro' in row else ''
    acting_region.address = row['endereco'] if 'endereco' in row else ''

    if acting_region.id == '':
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
    name_cli = row['consultor'] if 'consultor' in row else ''
    if name_cli is not None and name_cli != '':
        name_cli = name_cli.split('-')
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
    client.cnpj = row['cnpj'] if 'cnpj' in row else ''
    client.name = row['razao_social'] if 'razao_social' in row else ''

    if client.cnpj == '':
        client = None
    
    return client


def transform_sale(row: dict) -> Sale:
    sale = Sale()
    sale.nf = row['numero_pedido'] if 'numero_pedido' in row else ''
    if 'qtd_fat' in row and 'qtd_log_fat' in row and row['qtd_fat'] != '' and row['qtd_log_fat'] != '':
        sale.total_ammount = int(row['qtd_fat']) + int(row['qtd_log_fat'])
    else:
        sale.total_ammount = 0
    if 'valor_fat' in row and row['valor_fat'] != '':
        sale.total_value = process_currency_values(row['valor_fat'])
    if 'valor_log_fat' in row and row['valor_log_fat']:
        sale.total_value += process_currency_values(row['valor_log_fat'])
    else:
        sale.total_value = 0
    
    sale.date = row['data'] if 'data' in row else ''

    if sale.nf == '' and sale.date is None:
        sale = None

    return sale


def transform_characteristics(row: dict) -> Characteristics:
    """Realiza a etapa de transformação dos dados de características.

    Args
        row (dict) -- O registro a ser transformado.

    Returns
        Characteristics -- As características de clientes contidos na base lida.
    """
    characteristics = Characteristics()
    characteristics.company_cnpj = '84684620000187'
    characteristics.client_cnpj = row['cnpj'] if 'cnpj' in row else ''

    characteristics.name_array = [
        'Cat Xarope',
        'Cat Digestivos Líquidos',
        'Cat Digestivos Flaconetes',
        'Cat Polivitamínicos',
        'Cat Fitovital'
    ]
    characteristics.order_array = [1, 2, 3, 4, 5]
    characteristics.value_array = [
        row['cat_xarope'],
        row['cat_diges_liquidos'],
        row['cat_diges_flaconetes'],
        row['cat_polivitaminicos'],
        row['cat_fitovital'],
    ]
    
    return characteristics
