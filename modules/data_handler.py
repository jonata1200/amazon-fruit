# imports no topo (confira se já tem)
import sqlite3
import pandas as pd
from typing import Optional, Tuple

# mapeia a coluna de data primária por tabela (ajuste se necessário)
_TABLE_DATE_COL = {
    "Financas": "Data",
    "Fornecedores": "Data_Ultima_Compra",
    "Recursos_Humanos": "Data_Contratacao",
    # Estoque e Publico_Alvo normalmente não são dirigidos por "evento" diário.
    # Se quiser, você pode adicionar "Estoque": "Data_Validade"
}

class DataHandler:
    def __init__(self, db_path: str = 'amazon_fruit.db', conn: Optional[sqlite3.Connection] = None):
        self.db_path = db_path
        self.conn = conn
        # estado do filtro de período (YYYY-MM-DD)
        self._period: Optional[Tuple[str, str]] = None

    # ---------- período ----------
    def set_period(self, start_date_iso: str, end_date_iso: str):
        """Define um período global (inclusive) no formato YYYY-MM-DD."""
        self._period = (start_date_iso, end_date_iso)

    def clear_period(self):
        """Remove o filtro de período."""
        self._period = None

    def get_period(self) -> Optional[Tuple[str, str]]:
        return self._period

    # ---------- conexão ----------
    def _get_connection(self) -> sqlite3.Connection:
        return self.conn if self.conn is not None else sqlite3.connect(self.db_path)

    def _table_exists(self, conn: sqlite3.Connection, table: str) -> bool:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1;", (table,))
        return cur.fetchone() is not None

    # ---------- leitura com período automático ----------
    def load_table(self, table_name: str) -> pd.DataFrame:
        """
        Lê a tabela inteira OU filtrada por período se houver coluna de data mapeada
        e um período global definido via set_period().
        """
        table = table_name  # já padronizado no seu projeto
        with self._get_connection() as conn:
            if not self._table_exists(conn, table):
                return pd.DataFrame()

            # monta SQL
            date_col = _TABLE_DATE_COL.get(table)
            params = {}
            if date_col and self._period:
                start, end = self._period
                sql = f"""
                    SELECT * FROM {table}
                    WHERE date({date_col}) BETWEEN date(:start) AND date(:end)
                """
                params = {"start": start, "end": end}
            else:
                sql = f"SELECT * FROM {table}"

            df = pd.read_sql_query(sql, conn, params=params)

        # parse de datas consistente (sem warnings)
        for col in df.columns:
            if 'Data' in col or 'data' in col:
                df[col] = pd.to_datetime(df[col], errors='coerce', format='%Y-%m-%d')
        return df

    def get_dataframe(self, table_name: str):
        """
        Compatibilidade com código legado.
        Agora delega para load_table(), que já aplica o filtro de período (se definido).
        """
        return self.load_table(table_name)

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