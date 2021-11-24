"""Este módulo contém a definição de um vendedor."""


from src.models.base import BaseModel
from src.models.entities.company import Company
from src.models.util import process_text


class Salesperson(BaseModel):
    """Representa um vendedor."""

    def __init__(self) -> None:
        super().__init__()

        self.__internal_id = ''
        self.__name = ''
        self.company_cnpj = ''
        self.table_name = 'salesperson'

    
    @property
    def internal_id(self) -> str:
        """Método getter para o ID interno do vendedor para a empresa onde o
        vendedor trabalha.
        
        Returns
            str -- O ID do vendedor.
        """
        return self.__internal_id


    @internal_id.setter
    def internal_id(self, internal_id: str) -> None:
        """Método setter para o ID interno do vendedor para a empresa onde o
        vendedor trabalha.
        
        Args
            internal_id (str) -- O ID do vendedor.

        Returns
            None.
        """
        self.__internal_id = process_text(internal_id)

    
    @property
    def name(self) -> str:
        """Método getter para o nomedo vendedor.
        
        Returns
            str -- O nome do vendedor.
        """
        return self.__name


    @name.setter
    def name(self, name: str) -> None:
        """Método setter para o nome do vendedor.
        
        Args
            name (str) -- O nome do vendedor

        Returns
            None.
        """
        self.__name = process_text(name)

    
    def references_company(self, company: Company) -> None:
        """Extrai e insere a referência à empresa para a qual o vendedor
        trabalha.
        
        Args
            company (Company) -- A empresa para a qual o vendedor trabalha.

        Returns
            None.
        """
        self.company_cnpj = company.cnpj

    
    def to_dict(self) -> dict:
        return {
            'internal_id': self.internal_id,
            'name': self.name,
            'company_cnpj': self.company_cnpj
        }
