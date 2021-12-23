"""Este módulo contém funções comuns para utilização nos módulos de modelos."""

import datetime

from typing import Any, List


def process_cnpj(cnpj: str) -> str:
    """Realiza o processamento do CNPJ.
    
    Args
        cnpj (str) -- O CNPJ a ser processado.

    Returns
        str -- O CNPJ processado.
    """
    if isinstance(cnpj, str):
        return cnpj \
            .replace('.', '') \
            .replace('/', '') \
            .replace('-', '')
    return ''

def process_text(text: str) -> str:
    """Realiza o processamento do texto passado.
    
    Args
        text (str) -- O texto a ser processado.

    Returns
        str -- O texto processado.
    """
    if isinstance(text, str):
        return text \
            .lower() \
            .replace('á', 'a') \
            .replace('é', 'e') \
            .replace('í', 'i') \
            .replace('ó', 'o') \
            .replace('ú', 'u') \
            .replace('â', 'a') \
            .replace('ê', 'e') \
            .replace('ã', 'a') \
            .replace('õ', 'o') \
            .replace('ç', 'c')

    return ''


def preprocess_insert_values_text(texts: List[str]) -> List[str]:
    """Realiza o pré-processamento do texto antes de enviá-lo para a consulta
    no banco de dados. Isso é feito para evitar que caracteres tais como uma
    aspa simples gere um erro.
    
    Args
        text (str) -- O texto a ser pré-processado.

    Returns
        str -- O texto pré-processado.
    """
    return [ text.replace("'", "''") for text in texts ]


def process_currency_values(value: str) -> float:
    """Processa o valor monetário a partir da string.
    O padrão aceito é um valor com casa decimal separado por vírgula.
    
    Args
        value (str) -- O valor a ser processado.

    Returns
        float -- O valor processado.
    """
    value = value.replace(',', '.')
    value = float(value)

    return value


def process_date(date: str) -> datetime.date:
    try:
        date = datetime.datetime.strptime(date, '%d/%m/%Y').date()
    except:
        date = None
    
    return date


def as_array(array: List[Any]):
    array = [ str(value) for value in array ]
    return '{' + ', '.join(array) + '}'
