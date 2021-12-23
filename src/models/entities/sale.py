"""Este módulo contém a definição de uma venda."""

import datetime
from src.models.util import process_date, process_text
from src.models.base import BaseModel
from src.models.entities.client import Client
from src.models.entities.salesperson import Salesperson
from src.models.entities.product import Product

class Sale(BaseModel):
    """Representa uma venda realizada."""

    def __init__(self) -> None:
        super().__init__()
        self.id = ''
        self.__nf = ''
        self.__total_ammount = ''
        self.__total_value = ''
        self.__date = ''
        self.client_cnpj = ''
        self.product_id = ''
        self.salesperson_internal_id = ''
        self.salesperson_name = ''
        self.table_name = 'sale'

    
    @property
    def id(self) -> str:
        if self.__id == '':
            self.__id = str(abs(hash(f'{self.nf}{self.total_ammount}{self.total_value}{self.date}'))).zfill(20)
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id


    @property
    def nf(self) -> str:
        return self.__nf


    @nf.setter
    def nf(self, nf: str) -> None:
        self.__nf = process_text(nf)


    @property
    def total_ammount(self) -> int:
        return self.__total_ammount


    @total_ammount.setter
    def total_ammount(self, total_ammount: int) -> None:
        self.__total_ammount = total_ammount


    @property
    def total_value(self) -> float:
        return self.__total_value


    @total_value.setter
    def total_value(self, total_value: str) -> None:
        self.__total_value = total_value


    @property
    def date(self) -> datetime.date:
        return self.__date


    @date.setter
    def date(self, date: str) -> None:
        self.__date = process_date(date)


    def references_salesperson(self, salesperson: Salesperson) -> None:
        self.salesperson_internal_id = salesperson.internal_id
        self.salesperson_name = salesperson.name


    def references_product(self, product: Product) -> None:
        self.product_id = product.internal_id


    def references_client(self, client: Client) -> None:
        self.client_cnpj = client.cnpj


    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nf': self.nf,
            'total_ammount': self.total_ammount,
            'total_value': self.total_value,
            'date': self.date,
            'client_cnpj': self.client_cnpj,
            'product_internal_id': self.product_id,
            'salesperson_internal_id': self.salesperson_internal_id,
            'salesperson_name': self.salesperson_name
        }
