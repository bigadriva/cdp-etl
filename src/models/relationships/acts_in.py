"""Este módulo contém a definição de uma relação "ACTS IN"."""

from src.models.base import BaseModel
from src.models.entities.salesperson import Salesperson
from src.models.entities.acting_region import ActingRegion


class ActsIn(BaseModel):
    """Representa um relacionamento de "ACTS IN"."""

    def __init__(self) -> None:
        """Inicializa uma instância do relacionamento."""
        super().__init__()

        self.salesperson_internal_id = ''
        self.salesperson_name = ''
        self.acting_region_city = ''
        self.acting_region_address = ''
        self.table_name = 'acts_in'

    
    def references_salesperson(self, salesperson: Salesperson) -> None:
        """Extrai e insere a referência ao vendedor que atua em uma região.

        Args
            salesperson (Salesperson) -- O vendedor.

        Returns
            None.
        """
        self.salesperson_internal_id = salesperson.internal_id
        self.salesperson_name = salesperson.name

    
    def references_acting_region(self, acting_region: ActingRegion) -> None:
        """Extrai e insere a referência à região de atuação de um vendedor.

        Args
            acting_region (ActingRegion) -- A região de atuação.

        Returns
            None.
        """
        self.acting_region_city = acting_region.city
        self.acting_region_address = acting_region.address


    def to_dict(self) -> dict:
        return {
            'salesperson_internal_id': self.salesperson_internal_id,
            'salesperson_name': self.salesperson_name,
            'acting_region_city': self.acting_region_city,
            'acting_region_address': self.acting_region_address,
        }
