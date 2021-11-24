"""Este módulo contém a definição de um produto."""

from src.models.util import process_text
from src.models.base import BaseModel


class Product(BaseModel):
    """Representa um produto vendido por uma empresa."""

    def __init__(self) -> None:
        super().__init__()

        self.__internal_id = None
        self.__name = ''
        self.__type = ''
        self.table_name = 'product'


    @property
    def internal_id(self) -> str:
        """Método getter para o ID interno do produto na empresa.
        
        Returns
            str -- O ID interno do produto na empresa.
        """
        return self.__internal_id


    @internal_id.setter
    def internal_id(self, internal_id: str) -> None:
        """Método getter para o ID interno do produto na empresa.
        
        Args
            str -- O ID interno do produto na empresa.

        Returns
            None.
        """
        internal_id = process_text(internal_id)
        self.__internal_id = internal_id


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
        self.__name = process_text(name)


    @property
    def type(self) -> str:
        """Método getter para o tipo de produto de acordo com a empresa.
        
        Returns
            str -- O tipo de produto de acordo com a empresa.
        """
        return self.__type


    @type.setter
    def type(self, _type: str) -> None:
        """Método setter para o tipo de produto de acordo com a empresa.
        
        Args
            str -- O tipo de produto de acordo com a empresa.

        Returns
            None.
        """
        self.__type = process_text(_type)


    def to_dict(self) -> dict:
        return {
            'internal_id': self.internal_id,
            'name': self.name,
            'type': self.type,
        }
