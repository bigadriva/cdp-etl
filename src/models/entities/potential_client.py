"""Este módulo contém a definição de um cliente."""

from src.models.base import BaseModel
from src.models.entities.acting_region import ActingRegion
from src.models.util import process_cnpj, process_text


class PotentialClient(BaseModel):
    """Representa um cliente."""
    def __init__(self) -> None:
        """Inicializa uma instância do cliente."""
        super().__init__()

        self.__cnpj = ''
        self.__name = ''
        self.acting_region_id = ''
        self.table_name = 'potential_client'


    @property
    def cnpj(self) -> str:
        """Método getter para o CNPJ do cliente.
        
        Returns
            str -- O CNPJ do cliente.
        """
        return self.__cnpj


    @cnpj.setter
    def cnpj(self, cnpj: str) -> None:
        """Método setter para o CNPJ do cliente.
        Antes de enviar ao banco, realiza o processamento do CNPJ:
            - Retira caracteres não-numéricos
            - Padroniza com 14 dígitos, inserindo zeros à esquerda, se
            necessário.

        Args
            cnpj (str) -- O CNPJ do cliente.

        Returns
            None.
        """
        cnpj = process_cnpj(cnpj)

        self.__cnpj = cnpj.zfill(14)


    @property
    def name(self) -> str:
        """Método getter para o nome do cliente.
        
        Returns
            str -- O nome do cliente
        """
        return self.__name


    @name.setter
    def name(self, name: str) -> None:
        """Método setter para o nome do cliente.
        Antes de enviar ao banco, realiza o processamento do nome:
            - Retira acentos tônicos
            - Troca 'ç' por 'c'

        Args
            name (str) -- O nome do cliente.

        Returns
            None.
        """
        name = process_text(name)
            
        self.__name = name
        
    def references_acting_region(self, acting_region: ActingRegion) -> None:
        """Extrai e insere a referência à região de atuação no objeto de
        cliente.
        
        Args
            acting_region (ActingRegion) -- A região na qual um cliente está.

        Returns
            None.
        """
        self.acting_region_id = acting_region.id


    def to_dict(self) -> dict:
        return {
            'cnpj': self.cnpj,
            'name': self.name,
            'acting_region_id': self.acting_region_id,
        }
