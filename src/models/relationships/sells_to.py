"""Este módulo contém a definição de uma relação "SELLS TO"."""

from src.models.base import BaseModel
from src.models.entities.client import Client
from src.models.entities.salesperson import Salesperson


class SellsTo(BaseModel):
    """Representa um relacionamento de "SELLS TO"."""

    def __init__(self) -> None:
        """Inicializa uma instância do relacionamento."""
        super().__init__()

        self.client_cnpj = ''
        self.salesperson_internal_id = ''
        self.salesperson_name = ''
        self.table_name = 'sells_to'


    def references_client(self, client: Client) -> None:
        """Extrai e insere a referência ao cliente que compra do vendedor.
        
        Args
            client (Client) -- O cliente.

        Returns
            None.
        """
        self.client_cnpj = client.cnpj


    def references_salesperson(self, salesperson: Salesperson) -> None:
        """Extrai e insere a referência ao cliente que compra do vendedor.
        
        Args
            client (Client) -- O cliente.

        Returns
            None.
        """
        self.salesperson_internal_id = salesperson.internal_id
        self.salesperson_name = salesperson.name

    
    def to_dict(self) -> dict:
        return {
            'client_cnpj': self.client_cnpj,
            'salesperson_internal_id': self.salesperson_internal_id,
            'salesperson_name': self.salesperson_name
        }
