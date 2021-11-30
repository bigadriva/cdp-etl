"""Este módulo contém a definição de um cliente."""

import re

from typing import List
from src.models.base import BaseModel
from src.models.entities.company import Company
from src.models.entities.client import Client
from src.models.util import as_array, process_text


class Characteristics(BaseModel):
    """Representa um cliente."""
    def __init__(self) -> None:
        """Inicializa uma instância do cliente."""
        super().__init__()

        self.__name_array = ''
        self.__value_array: List[float] = []
        self.__order_array: List[int] = []
        self.company_cnpj = ''
        self.client_cnpj = ''
        self.table_name = 'characteristics'


    @property
    def name_array(self) -> List[str]:
        # Retornamos uma string para manter o padrão na hora de gerar as
        # consultas de inserção.
        # Uma consulta de inserção de vetor no banco (postgres) é como o
        # seguinte exemplo:
        # INSERT INTO table
        #   (cnpj, name_array, value_array)
        #   VALUES ('123456789-cnpj', '{"matheus", "bigarelli"}', '{0, 1, 2}')
        # Então, o resultado desse GET tem de ser algo como:
        # {"categoria de xarope", "categoria de flaconetes", "categoria de fitovital"}
        return as_array(self.__name_array)


    @name_array.setter
    def name_array(self, names: List[str]) -> None:
        names = [ process_text(name) for name in names ]

        self.__name_array = names


    @property
    def value_array(self) -> str:
        # Retornamos uma string para manter o padrão na hora de gerar as
        # consultas de inserção.
        # Uma consulta de inserção de vetor no banco (postgres) é como o
        # seguinte exemplo:
        # INSERT INTO table
        #   (cnpj, name_array, value_array)
        #   VALUES ('123456789-cnpj', '{"matheus", "bigarelli"}', '{0, 1, 2}')
        # Então, o resultado desse GET tem de ser algo como: {0, 1, 2}
        return as_array(self.__value_array)


    @value_array.setter
    def value_array(self, values: List[str]) -> None:
        try:
            values = [ float(re.search(r'\d+', value).group(0)) for value in values ]
        except:
            values = []

        self.__value_array = values


    @property
    def order_array(self) -> List[int]:
        # Retornamos uma string para manter o padrão na hora de gerar as
        # consultas de inserção.
        # Uma consulta de inserção de vetor no banco (postgres) é como o
        # seguinte exemplo:
        # INSERT INTO table
        #   (cnpj, name_array, value_array)
        #   VALUES ('123456789-cnpj', '{"matheus", "bigarelli"}', '{0, 1, 2}')
        # Então, o resultado desse GET tem de ser algo como: {0, 1, 2}
        return as_array(self.__order_array)


    @order_array.setter
    def order_array(self, order: List[int]) -> None:
        self.__order_array = order
        

    def references_company(self, company: Company) -> None:
        """Extrai e insere a referência à empresa que deu a característica ao
        cliente.
        
        Args
            company (Company) -- A empresa que deu a característica.

        Returns
            None.
        """
        self.company_cnpj = company.cnpj
        

    def references_client(self, client: Client) -> None:
        """Extrai e insere a referência à empresa que possui a característica.
        
        Args
            client (Client) -- A empresa que recebeu a característica.

        Returns
            None.
        """
        self.client_cnpj = client.cnpj


    def to_dict(self) -> dict:
        return {
            'name_array': self.name_array,
            'value_array': self.value_array,
            'order_array': self.order_array,
            'company_cnpj': self.company_cnpj,
            'client_cnpj': self.client_cnpj,
        }
