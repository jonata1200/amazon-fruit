# modules/data_handler.py

import pandas as pd
import sqlite3

class DataHandler:
    """
    Classe responsável por carregar e gerenciar os dados
    do banco de dados SQLite da Amazon Fruit.
    """
    def __init__(self, db_path='amazon_fruit.db'):
        self.db_path = db_path

    def _get_connection(self):
        """Retorna uma conexão com o banco de dados."""
        return sqlite3.connect(self.db_path)

    def get_dataframe(self, table_name):
        """
        Lê uma tabela inteira do banco de dados e a retorna como um DataFrame.
        """
        try:
            with self._get_connection() as conn:
                # O Pandas consegue ler uma query SQL diretamente para um DataFrame
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                # Converte colunas de data/hora se existirem
                for col in df.columns:
                    if 'Data' in col:
                        df[col] = pd.to_datetime(df[col])
                return df
        except Exception as e:
            print(f"Ocorreu um erro ao ler a tabela '{table_name}': {e}")
            return pd.DataFrame() # Retorna um DataFrame vazio em caso de erro

    def execute_query(self, query, params=()):
        """
        Executa uma query de modificação (INSERT, UPDATE, DELETE).
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao executar a query: {e}")
            return False

    def add_record(self, table_name, data_dict):
        """
        Adiciona um novo registro a uma tabela.
        `data_dict` é um dicionário onde as chaves são os nomes das colunas.
        """
        columns = ', '.join(data_dict.keys())
        placeholders = ', '.join(['?'] * len(data_dict))
        values = tuple(data_dict.values())
        
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        return self.execute_query(query, values)

    def update_record(self, table_name, data_dict, identifier_col, identifier_val):
        """
        Atualiza um registro existente em uma tabela.
        """
        set_clause = ', '.join([f"{key} = ?" for key in data_dict.keys()])
        values = tuple(data_dict.values()) + (identifier_val,)

        query = f"UPDATE {table_name} SET {set_clause} WHERE {identifier_col} = ?"
        return self.execute_query(query, values)