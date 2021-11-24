"""Este módulo contém a definição do modelo base utilizado no projeto"""

from src.models.util import preprocess_insert_values_text


class BaseModel:
    def upload_to_db(self, conn) -> None:
        """Realiza o upload do modelo para o banco de dados.
        
        Args
            conn (psycopg2.connection) -- A conexão com o banco de dados.

        Returns
            None
        """
        data = self.to_dict()
        table_name = self.table_name
        with conn.cursor() as cursor:
            items = data.items()
            # Mágica para tirar pares onde o valor é nulo             |
            #                                                         V
            # { 'cnpj': '12345678901234', 'vendedor': 'asdf', 'nome': '' }
            items = list(zip(*filter(lambda x: x[1], items)))
            attributes = items[0]
            values = items[1]

            values = preprocess_insert_values_text(values)

            # Só carregamos no banco dados não vazios
            if values:
                # Se não houver chaves estrangeiras a serem associadas,
                # podemos simplesmente jogar no banco.
                att_str = ", ".join(attributes)

                val_str = "'" + "', '".join(values) + "'"
                
                insert_query = f'''
                INSERT INTO {table_name} ({att_str})
                VALUES ({val_str})
                ON CONFLICT DO NOTHING
                '''

                cursor.execute(insert_query)


    def to_dict(self) -> dict:
        """Realiza a transformação do modelo para um dicionário.
        
        Returns
            dict -- O modelo em formato dicionário { 'atributo': 'valor' }.
        """
        # Cada subclasse deve ter o seu implementado
        message = ''
        message += '[ BASEMODEL.TO_DICT ] Este método é um placeholder.'
        message += 'Implemente na subclasse.'
        raise NotImplementedError(message)
