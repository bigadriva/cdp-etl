"""Este módulo contém a definição de uma relação "SELLS"."""

import pandas as pd

from src.models.base import BaseModel
from src.models.entities.salesperson import Salesperson
from src.models.entities.product import Product
from src.models.util import process_currency_values


class Sells(BaseModel):
    """Representa um relacionamento de "SELLS"."""

    def __init__(self) -> None:
        """Inicializa uma instância do relacionamento."""
        super().__init__()

        self.salesperson_internal_id = ''
        self.salesperson_name = ''
        self.product_internal_id = ''
        self.__date = ''
        self.__value = 0
        self.table_name = 'sells'


    @property
    def date(self) -> pd.Timestamp:
        return self.__date

    @date.setter
    def date(self, date: str):
        # Há vários formatos na base da catarinense, sendo os detectados:
        #   - 12/11/2021
        self.__date = str(pd.to_datetime(date, format='%d/%m/%Y').date())


    @property
    def value(self) -> str:
        # Retornamos como string para padronizar a lista de valores passadas
        # para a etapa de LOAD. Não mexer. Se mexer, vai dar problema.
        return str(self.__value)

    @value.setter
    def value(self, value: str):
        if isinstance(value, str):
            self.__value = process_currency_values(value)
        else:
            self.__value = value

    
    def references_salesperson(self, salesperson: Salesperson) -> None:
        """Extrai e insere a referência à empresa para a qual o vendedor
        trabalha.
        
        Args
            company (Company) -- A empresa para a qual o vendedor trabalha.

        Returns
            None.
        """
        self.salesperson_internal_id = salesperson.internal_id
        self.salesperson_name = salesperson.name

    
    def references_product(self, product: Product) -> None:
        """Extrai e insere a referência à empresa para a qual o vendedor
        trabalha.
        
        Args
            company (Company) -- A empresa para a qual o vendedor trabalha.

        Returns
            None.
        """
        self.product_internal_id = product.internal_id

    
    def to_dict(self) -> dict:
        return {
            'salesperson_internal_id': self.salesperson_internal_id,
            'salesperson_name': self.salesperson_name,
            'product_internal_id': self.product_internal_id,
            'date': self.date,
            'value': self.value
        }


    def __repr__(self) -> str:
        return f'''
            salesperson_internal_id: {self.salesperson_internal_id},
            salesperson_name: {self.salesperson_name},
            product_internal_id: {self.product_internal_id},
            date: {self.date},
        '''
