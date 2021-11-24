"""O propósito deste módulo é extrair os dados do CSV do close up e inserir no
banco de dados."""


import pandas as pd


def insert_close_up_in_db():
    """Insere o close up no banco de dados."""
    close_up = pd.read_csv('data/close-up.csv')
