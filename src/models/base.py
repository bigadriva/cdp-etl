"""Este módulo contém a definição do modelo base utilizado no projeto"""

import datetime
import os

from src.models.util import preprocess_insert_values_text


class BaseModel:
    def upload_to_db(self, cursor) -> None:
        """Realiza o upload do modelo para o banco de dados.
        
        Args
            cursor -- O cursor da conexão com o banco de dados.

        Returns
            None
        """
        data = self.to_dict()
        table_name = self.table_name
        try:
            items = data.items()
            # Mágica para tirar pares onde o valor é nulo             |
            #                                                         V
            # { 'cnpj': '12345678901234', 'vendedor': 'asdf', 'nome': '' }
            items = list(zip(*filter(lambda x: x[1], items)))
            attributes = items[0]
            values = items[1]

            # values = preprocess_insert_values_text(values)
            # Só carregamos no banco dados não vazios
            if values:
                # Se não houver chaves estrangeiras a serem associadas,
                # podemos simplesmente jogar no banco.
                att_str = ', '.join(attributes)

                # val_str = "'" + "', '".join(values) + "'"
                val_str = ''
                for i, val in enumerate(values):
                    if isinstance(val, str):
                        # Temos que escapar as aspas simples para não gerar
                        # problemas na consulta SQL. O postgres usa aspas
                        # simples para delimitar strings.
                        text = val.replace("'", "''")
                        val_str += f"'{text}'"

                    elif isinstance(val, datetime.date):
                        val_str += f"'{val}'"

                    elif isinstance(val, int) or isinstance(val, float):
                        val_str += f"{val}"
                    if i < len(values) - 1:
                        val_str += ', '
                
                insert_query = f'INSERT INTO {os.getenv("POSTGRES_SCHEMA")}.{table_name} ({att_str}) VALUES ({val_str}) ON CONFLICT DO NOTHING'

                cursor.execute(insert_query)
        except Exception as e:
            print(self.table_name)
            print(data)
            print(e)
            raise Exception('Aqui')


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
