import os

import pandas as pd


def create_catarinense_data():

    dados = pd.read_csv("/app/data/catarinense/dados_driva.csv", sep=";", dtype={
                        'CNPJ': str, 'VAL_FAT': float}, decimal=",")
    vend = pd.read_csv("/app/data/catarinense/vend_driva.csv", sep=";")
    prod = pd.read_csv("/app/data/catarinense/prod_driva.csv", sep=";")

    dados = dados[dados['RAZAO SOCIAL'].notnull()]
    dados_merge = pd.merge(dados, vend,
                        how="left", left_on="VEND_NF", right_on="VEND_CLI")
    dados_merge = pd.merge(dados_merge, prod,
                        how="left", left_on="COD", right_on="CODIGO")

    dados_selected = dados_merge[[
        'CNPJ', 'AREA_CLI', 'NOME_VEND_CLI', 'RAZAO SOCIAL', 'DATA', 'QTD_FAT',
        'QTD_LOG_FAT', 'VAL_FAT', 'VAL_LOG_FAT', 'PRODUTO'
    ]]
    
    dados_selected['CNPJ'] = dados_selected.apply(lambda row: row['CNPJ'].zfill(14), axis=1)
    dados_selected.DATA = pd.to_datetime(dados_selected.DATA, dayfirst=True)

    dados_selected = dados_selected.rename(columns={"CNPJ": "cnpj", "AREA_CLI": "area_client", "NOME_VEND_CLI": "consultor", "RAZAO SOCIAL": "razao_social",
                                                    "DATA": "data", "QTD_FAT": "qtd_s_refat", "QTD_LOG_FAT": "qtd_ol", "VAL_FAT": "valor_fat", 'VAL_LOG_FAT': 'valor_ol', "PRODUTO": "produto"})


    return dados_selected


def create_close_up():
    """Insere os dados do close up no Postgres."""
    types = {
        'CNPJ_PDV': str,
        'QTD. OL. (UND)': float,
        'QTD.S/REFAT. (UND)': float,
    }

    dados = pd.read_csv("/app/data/close-up.csv", dtype=types)
    dados = dados.rename(columns={
        column: column.lower().replace(' ', '_') for column in dados
    })

    dados['cnpj_pdv'] = dados['cnpj_pdv'].apply(lambda cnpj: cnpj.zfill(14))
    
    dados.rename({
        'QTD. OL. (UND)'.lower(): 'qtd_ol',
        'QTD.S/REFAT. (UND)'.lower(): 'qtd_s_refat'
    })


    return dados


def create_acting_region():
    pass


def create_client():
    pass


def create_company():
    pass


def create_product():
    pass


def create_sale():
    pass


def create_salesperson():
    pass


if __name__ == '__main__':
    create_catarinense_data()
