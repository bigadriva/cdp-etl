"""Este módulo contém a definição de uma empresa."""

from src.models.util import process_cnpj
from src.models.base import BaseModel


class Company(BaseModel):
    """Representa uma empresa cliente da Driva."""

    def __init__(self) -> None:
        super().__init__()

        self.__cnpj = ''
        self.__name = ''
        self.table_name = 'company'


    @property
    def cnpj(self) -> str:
        """Método getter para o CNPJ da empresa.
        
        Returns
            str -- O CNPJ da empresa.
        """
        return self.__cnpj


    @cnpj.setter
    def cnpj(self, cnpj: str) -> None:
        """Método getter para o CNPJ da empresa.
        
        Args
            str -- O CNPJ da empresa.

        Returns
            None.
        """
        cnpj = process_cnpj(cnpj)
        self.__cnpj = cnpj


    @property
    def name(self) -> str:
        """Método getter para o nome da empresa.
        
        Returns
            str -- O nome da empresa.
        """
        return self.__name


    @name.setter
    def name(self, name: str) -> None:
        """Método setter para o nome da empresa.
        
        Args
            str -- O nome da empresa.

        Returns
            None.
        """
        self.__name = name


    def to_dict(self) -> dict:
        """Transforma a empresa em um dicionário.
        
        Returns
            dict -- A empresa em formato de dicionário.
        """
        return {
            'cnpj': self.cnpj,
            'name': self.name
        }
