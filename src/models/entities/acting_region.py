"""Este módulo contém a definição de uma região de atuação."""

from src.models.base import BaseModel
from src.models.util import process_text


class ActingRegion(BaseModel):
    """Representa uma região de atuação."""

    def __init__(self) -> None:
        """Inicializa uma instância do cliente."""
        super().__init__()

        self.__id = ''
        self.__city = ''
        self.__neighborhood = ''
        self.__address = ''
        self.table_name = 'acting_region'


    @property
    def id(self) -> str:
        """Método getter para o id da região de atuação.
        
        Returns
            str -- O id da região de atuação.
        """
        if self.__id == '' and (self.city != '' or self.neighborhood != '' or self.address != ''):
            self.__id = str(abs(hash(self.city + self.neighborhood + self.address)))
            if self.__id != '':
                self.__id = self.__id.zfill(20)
            
        return self.__id


    @property
    def city(self) -> str:
        """Método getter para a cidade da região de atuação.
        
        Returns
            str -- O CNPJ do cliente.
        """
        return self.__city


    @city.setter
    def city(self, city: str) -> None:
        """Método setter para a cidade da região de atuação.

        Args
            city (str) -- A cidade da região de atuação.

        Returns
            None.
        """
        city = process_text(city)

        self.__city = city[:min(100, len(city))]


    @property
    def neighborhood(self) -> str:
        """Método getter para a cidade da região de atuação.
        
        Returns
            str -- O CNPJ do cliente.
        """
        return self.__neighborhood


    @neighborhood.setter
    def neighborhood(self, neighborhood: str) -> None:
        """Método setter para o bairro da cidade da região de atuação.

        Args
            neighborhood (str) -- O bairro da cidade da região de atuação.

        Returns
            None.
        """
        neighborhood = process_text(neighborhood)

        self.__neighborhood = neighborhood[:100]


    @property
    def address(self) -> str:
        """Método getter para o endereço da região de atuação. O endereço é
        composto de tipo de logradouro (rua, avenida, etc), nome do logradouro
        (Padre Anchieta, Comendador Araújo, etc) e número.
        Um exemplo de endereço pode ser: Avenida Batel, 287
        
        Returns
            str -- O endereço da região de atuação.
        """
        return self.__address


    @address.setter
    def address(self, address: str) -> None:
        """Método getter para o endereço da região de atuação. O endereço é
        composto de tipo de logradouro (rua, avenida, etc), nome do logradouro
        (Padre Anchieta, Comendador Araújo, etc) e número.
        Um exemplo de endereço pode ser: Avenida Batel, 287

        Args
            address (str) -- O endereço da região de atuação.

        Returns
            None.
        """
        address = process_text(address)

        self.__address = address[:100]


    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'city': self.city,
            'neighborhood': self.neighborhood,
            'address': self.address,
        }
