"""Este módulo contém a definição de uma região de atuação."""

from src.models.base import BaseModel
from src.models.util import process_text


class ActingRegion(BaseModel):
    """Representa uma região de atuação."""

    def __init__(self) -> None:
        """Inicializa uma instância do cliente."""
        super().__init__()

        self.__uf = ''
        self.__city = ''
        self.__neighborhood = ''
        self.__address = ''
        self.table_name = 'acting_region'


    @property
    def uf(self) -> str:
        """Método getter para a cidade da região de atuação.
        
        Returns
            str -- O CNPJ do cliente.
        """
        return self.__uf


    @uf.setter
    def uf(self, uf: str) -> None:
        """Método setter para a UF da região de atuação.

        Args
            uf (str) -- A UF da região de atuação.

        Returns
            None.
        """
        uf = process_text(uf)

        self.__uf = uf


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

        self.__city = city


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

        self.__neighborhood = neighborhood


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

        self.__address = address


    def to_dict(self) -> dict:
        return {
            'city': self.city,
            'neighborhood': self.neighborhood,
            'address': self.address,
        }
