import os
import pandas as pd

from elasticsearch import Elasticsearch


SERVERS = ['https://elastic.datadriva.com']
HTTP_AUTH = ('elastic', 'BvfrG2NHXFa9qm')


def enrich(data: pd.DataFrame):
    docs = get_city_data(data)
    data = add_city_info_to_data(data, docs)
    return data


def divide_list(l, n_elements):
    """Divide uma lista em M partes. Isso servirá para não sobrecarregar a consulta do elastic.
    Todas as requisições ao elastic não terão mais de N elementos, então dividiremos a lista
    recebida como parâmetro em M partes, cada uma com N elementos.
    :param l:list: A lista a ser dividida.
    :param n_elements:int: A quantidade máxima de elementos para cada parte.
    :returns divisions:list: Uma lista com as divisões (lista de listas), cada uma com N elementos.
    """

    divisions = []
    for i in range(0, len(l), n_elements):
        if i + n_elements < len(l):
            divisions.append(l[i:i+n_elements])
        else:
            divisions.append(l[i:])

    return divisions



def get_city_data(data: pd.DataFrame) -> list:
    """Pega dados de cidades sobre os dados passados."""

    # Pegando todos os CNPJs únicos da tabela de clientes.

    unique_cnpjs = list(data['cnpj'].unique())

    # Para não enviar tudo em uma única pesquisa, vamos dividir a consulta em 10 requisições.
    # Assim, temos aproximadamente 5 mil CNPJs por consulta.
    ids_split = divide_list(unique_cnpjs, 1000)

    docs = get_cities_from_elastic(ids_split)

    return docs


def add_city_info_to_data(data: pd.DataFrame, docs: list) -> dict:
    """Adiciona os dados de cidades do elastic a todos os dataframes passados como dado.
    :param data:dict: Um dicionário com dataframes indexados por nome.
    :param docs:list: Uma lista de documentos do elastic com os dados de cidades.
    :returns dict: Um dicionário com os dataframes atualizados com os dados de cidades.
    """
    data_complete = None
    # De posse dos dados de cidades, podemos agora criar um dataframe com esses dados e
    # trabalhar utilizando ele. No entanto, pode ser que nem todos os CNPJs foram
    # encontrados em apenas uma consulta.
    df_cities = pd.DataFrame([doc['_source']
                              for _docs in docs
                              for doc in _docs['docs']
                              if '_source' in doc])

    if not df_cities.empty:
        df_cities['cnpj'] = df_cities['cnpj'].astype('str').str.zfill(14)
        # Agora podemos inserir os dados de cidades nos dataframes
        data_complete = data.join(df_cities.set_index('cnpj'), on='cnpj')

    return data_complete


def get_cities_from_elastic(ids_split: list) -> list:
    """Busca dados de municípios no servidor do elastic search e retorna o resultado dividido por
    lista de ids
    :param ids_split:list: A lista de listas de ids (CNPJs) a serem buscados no elastic.
    :returns list: A lista com os documentos do elastic.
    """
    with Elasticsearch(hosts=SERVERS, http_auth=HTTP_AUTH) as elastic:
        docs = []
        for i, _ids in enumerate(ids_split):
            try:
                print('[ENRICH] Getting', i+1, 'of', len(ids_split))
                docs.append(elastic.mget(
                    body={'ids': _ids}, index='empresasdobrasilv12', _source=['cnpj', 'municipio', 'bairro', 'endereco']))
            except Exception as e:
                print(f'[ENRICH] Error:{e}')
    return docs
