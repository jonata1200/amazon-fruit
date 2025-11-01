# modules/data_handler.py

import pandas as pd
import sqlite3
from typing import Optional

# nomes tolerantes -> tabela real
_ALLOWED_TABLES = {
    "Estoque": "Estoque",
    "Fornecedores": "Fornecedores",
    "Publico_Alvo": "Publico_Alvo",
    "Público_Alvo": "Publico_Alvo",
    "Financas": "Financas",
    "Finanças": "Financas",
    "Recursos_Humanos": "Recursos_Humanos",
}

class DataHandler:
    """
    Classe responsável por carregar e gerenciar os dados
    do banco de dados SQLite da Amazon Fruit.
    """
    def __init__(self, db_path: str = 'amazon_fruit.db'):
        self.db_path = db_path

    # ---------------- utilitários de conexão ----------------
    def _get_connection(self) -> sqlite3.Connection:
        """Retorna uma conexão com o banco de dados."""
        return sqlite3.connect(self.db_path)

    # ---------------- utilitários internos ----------------
    def _resolve_table_name(self, name: str) -> str:
        """Mapeia variações de nome para o nome real da tabela."""
        return _ALLOWED_TABLES.get(name, name)

    def _table_exists(self, conn: sqlite3.Connection, table: str) -> bool:
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1;",
            (table,),
        )
        return cur.fetchone() is not None

    # ---------------- API pública (já existente) ----------------
    def get_dataframe(self, table_name: str) -> pd.DataFrame:
        """
        Lê uma tabela inteira do banco de dados e a retorna como um DataFrame.
        """
        try:
            with self._get_connection() as conn:
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                # Converte colunas que contenham 'Data' para datetime (quando fizer sentido)
                for col in df.columns:
                    if 'Data' in col:
                        df[col] = pd.to_datetime(df[col], errors='coerce', format='%Y-%m-%d')
                return df
        except Exception as e:
            print(f"Ocorreu um erro ao ler a tabela '{table_name}': {e}")
            return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

    # ---------------- NOVO: compatibilidade com report_generator ----------------
    def load_table(self, table_name: str) -> pd.DataFrame:
        """
        Compat layer para o report_generator e dashboards.
        - Aceita nomes com/sem acento.
        - Verifica existência da tabela antes de ler.
        """
        real_name = self._resolve_table_name(table_name)
        try:
            with self._get_connection() as conn:
                if not self._table_exists(conn, real_name):
                    # Evita exception de tabela inexistente
                    return pd.DataFrame()
            # Reutiliza a lógica existente (inclui parse de datas)
            return self.get_dataframe(real_name)
        except Exception as e:
            print(f"Erro em load_table('{table_name}'): {e}")
            return pd.DataFrame()

    # ---------------- operações de escrita ----------------
    def execute_query(self, query: str, params: tuple = ()) -> bool:
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

    def add_record(self, table_name: str, data_dict: dict) -> bool:
        """
        Adiciona um novo registro a uma tabela.
        `data_dict` é um dicionário onde as chaves são os nomes das colunas.
        """
        columns = ', '.join(data_dict.keys())
        placeholders = ', '.join(['?'] * len(data_dict))
        values = tuple(data_dict.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        return self.execute_query(query, values)

    def update_record(self, table_name: str, data_dict: dict,
                      identifier_col: str, identifier_val) -> bool:
        """
        Atualiza um registro existente em uma tabela.
        """
        set_clause = ', '.join([f"{key} = ?" for key in data_dict.keys()])
        values = tuple(data_dict.values()) + (identifier_val,)
        query = f"UPDATE {table_name} SET {set_clause} WHERE {identifier_col} = ?"
        return self.execute_query(query, values)
    
    def delete_record(self, table_name: str, identifier_col: str, identifier_val) -> bool:
        """
        Exclui um registro de uma tabela com base em uma coluna identificadora.
        """
        query = f"DELETE FROM {table_name} WHERE {identifier_col} = ?"
        params = (identifier_val,)
        return self.execute_query(query, params)
    
    def record_exists(self, table_name: str, column_name: str, value) -> bool:
        """
        Verifica se um registro com um valor específico em uma coluna já existe.
        Retorna True se existir, False caso contrário.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                query = f"SELECT COUNT(1) FROM {table_name} WHERE {column_name} = ?"
                cursor.execute(query, (value,))
                result = cursor.fetchone()[0]
                return result > 0
        except Exception as e:
            print(f"Erro ao verificar a existência do registro: {e}")
            # Em caso de erro, assuma True para evitar duplicação inadvertida
            return True