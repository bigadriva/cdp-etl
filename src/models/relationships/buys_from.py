"""Este módulo contém a definição de uma relação "BUYS FROM"."""

from src.models.base import BaseModel
from src.models.entities.company import Company
from src.models.entities.client import Client


class BuysFrom(BaseModel):
    """Representa um relacionamento de "BUYS FROM"."""

    def __init__(self) -> None:
        """Inicializa uma instância do relacionamento."""
        super().__init__()

        self.company_cnpj = ''
        self.client_cnpj = ''
        self.table_name = 'buys_from'

    
    def references_company(self, company: Company) -> None:
        """Extrai e insere a referência à empresa da qual o cliente compra.
        
        Args
            company (Company) -- A empresa.

        Returns
            None.
        """
        self.company_cnpj = company.cnpj

    
    def references_client(self, client: Client) -> None:
        """Extrai e insere a referência ao cliente que compra da empresa.
        
        Args
            client (Client) -- O cliente.

        Returns
            None.
        """
        self.client_cnpj = client.cnpj


    def to_dict(self) -> dict:
        return {
            'company_cnpj': self.company_cnpj,
            'client_cnpj': self.client_cnpj
        }
