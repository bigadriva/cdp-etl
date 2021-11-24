import os
import pandas as pd


from elasticsearch import Elasticsearch
SERVERS = ['https://kibana.datadriva.com/elastic']
HTTP_AUTH = ('elastic', '38HtYPA6Ss234is')


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


def add_cities(data: dict) -> dict:
    """Adiciona as cidades onde as empresas estão para cada CNPJ em todos os dataframes
    passados em um dicionário.
    :param data:dict: O dicionário com os dataframes aos quais se deseja que se adicione um campo
                      de cidade. É obrigatório que ele possua uma coluna contendo os CNPJs das
                      empresase que essa coluna seja nomeada como "cnpj".
    :returns data:dict: O dicionário com os dataframes enriquecidos com as cidades.
    """
    docs = get_city_data(data)
    data = add_city_info_to_data(data, docs)

    return data


def get_city_data(data: dict) -> list:
    """Pega dados de cidades sobre os dados passados.
    :param data:dict: Um dicionário com dataframes indexados por nome. Adicionaremos as cidades em
                      cada um deles.
    :returns list: Uma lista de documentos do elastic com os dados das cidades e CNPJs.
    """

    # Pegando todos os CNPJs únicos da tabela de clientes.
    df_clients = data[os.environ['SHEET_CLIENTS']]
    df_potentials = data[os.environ['SHEET_POTENTIALS']]

    unique_cnpjs = list(df_clients["cnpj"].unique(
    )) + list(df_potentials["cnpj_pdv"].unique())

    # Eliminando possíveis repetidos
    unique_cnpjs = list(set(unique_cnpjs))
    # Para não enviar tudo em uma única pesquisa, vamos dividir a consulta em 10 requisições.
    # Assim, temos aproximadamente 5 mil CNPJs por consulta.
    ids_split = divide_list(unique_cnpjs, 1000)

    docs = get_cities_from_elastic(ids_split)

    return docs


def add_city_info_to_data(data: dict, docs: list) -> dict:
    """Adiciona os dados de cidades do elastic a todos os dataframes passados como dado.
    :param data:dict: Um dicionário com dataframes indexados por nome.
    :param docs:list: Uma lista de documentos do elastic com os dados de cidades.
    :returns dict: Um dicionário com os dataframes atualizados com os dados de cidades.
    """
    df_clients = data[os.environ['SHEET_CLIENTS']]
    df_potentials = data[os.environ['SHEET_POTENTIALS']]
    # De posse dos dados de cidades, podemos agora criar um dataframe com esses dados e
    # trabalhar utilizando ele. No entanto, pode ser que nem todos os CNPJs foram
    # encontrados em apenas uma consulta.
    df_cities = pd.DataFrame([doc['_source']
                              for _docs in docs
                              for doc in _docs['docs']
                              if '_source' in doc])
    df_cities['cnpj'] = df_cities['cnpj'].astype('str').str.zfill(14)

    # Agora podemos inserir os dados de cidades nos dataframes
    df_clients_complete = df_clients.join(
        df_cities.set_index('cnpj'), on='cnpj')
    # No caso do dataframe de potenciais, ainda temos que renomear o campo de cidade novamente
    # para cidade_pdv, para manter os dados consistentes.
    df_potentials_complete = df_potentials.drop('cidade_pdv', axis=1) \
                                          .join(df_cities.set_index('cnpj'), on='cnpj_pdv') \
                                          .rename(columns={'municipio': 'cidade_pdv'})

    # Salvamos para a postereidade
    df_clients_complete
    df_potentials_complete

    # Agora montamos o retorno
    data[os.environ['SHEET_CLIENTS']] = df_clients_complete
    data[os.environ['SHEET_POTENTIALS']] = df_potentials_complete

    return data


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
                    body={'ids': _ids}, index='empresasdobrasilv10', _source=['cnpj', 'municipio', 'matriz_filial']))
            except Exception as e:
                print(f'[ENRICH] Error:{e}')
    return docs


def enrich(data):
    return add_cities(data)
