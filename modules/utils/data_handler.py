# modules/utils/data_handler.py

import sqlite3
import pandas as pd
from pathlib import Path

class DataHandler:
    def __init__(self, base_dir: Path | str | None = None):
     # Se um diretório base não for fornecido, calcula a partir do local deste arquivo.
     if base_dir is None:
         base_dir = Path(__file__).resolve().parents[2]
     
     # Constrói o caminho para o banco de dados de forma consistente.
     self.db_path = Path(base_dir) / "data" / "amazon_fruit.db"

     self.start_date: pd.Timestamp | None = None
     self.end_date: pd.Timestamp | None = None
     
     if not self.db_path.exists():
         raise FileNotFoundError(f"Arquivo de banco de dados não encontrado: {self.db_path}\nExecute o script de migração primeiro.")

    def _get_db_connection(self):
        """Cria e retorna uma conexão com o banco de dados SQLite."""
        return sqlite3.connect(self.db_path)

    def _map_name_to_table(self, name: str) -> str:
        """Mapeia o nome amigável para o nome real da tabela no banco de dados."""
        key = str(name).strip().lower().replace("_", "")
        mapping = {
            'financas': 'lancamentos_financeiros',
            'estoque': 'estoque_historico',
            'publicoalvo': 'clientes',
            'recursoshumanos': 'funcionarios',
            'fornecedores': 'fornecedores'
        }
        return mapping.get(key, '')

    def _get_date_column_for_table(self, table_name: str) -> str | None:
        """Retorna o nome da coluna de data para uma determinada tabela, se houver."""
        date_col_map = {
            'lancamentos_financeiros': 'Data',
            'estoque_historico': 'Data_Snapshot',
            'funcionarios': 'Data_Contratacao'
        }
        return date_col_map.get(table_name)

    def set_period(self, start_iso: str, end_iso: str):
        """Define o período de filtro para as próximas consultas."""
        self.start_date = pd.to_datetime(start_iso, errors='coerce')
        self.end_date = pd.to_datetime(end_iso, errors='coerce')

    def get_period(self) -> tuple[str, str] | None:
        if self.start_date and self.end_date:
            return self.start_date.strftime('%d/%m/%Y'), self.end_date.strftime('%d/%m/%Y')
        return None

    def load_table(self, name: str) -> pd.DataFrame:
        """Carrega uma tabela do banco de dados, aplicando o filtro de período se aplicável."""
        table_name = self._map_name_to_table(name)
        if not table_name:
            return pd.DataFrame()

        conn = self._get_db_connection()
        query = f"SELECT * FROM {table_name}"
        params = {}

        # O filtro de data é adicionado diretamente na consulta SQL - muito mais eficiente!
        date_col = self._get_date_column_for_table(table_name)
        if date_col and self.start_date and self.end_date:
            query += f" WHERE {date_col} BETWEEN :start_date AND :end_date"
            params = {'start_date': str(self.start_date), 'end_date': str(self.end_date)}
        
        try:
            # O Pandas lê diretamente o resultado da consulta SQL para um DataFrame.
            df = pd.read_sql_query(query, conn, params=params, parse_dates=[date_col] if date_col else None)
        finally:
            conn.close()
        
        return df

    def load_comparative_data(self, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Carrega dados para o período atual e o período anterior correspondente."""
        df_full = self.load_full_unfiltered_table(name) # Carrega tudo para calcular os períodos
        
        if df_full.empty:
            return pd.DataFrame(), pd.DataFrame()

        table_name = self._map_name_to_table(name)
        date_col = self._get_date_column_for_table(table_name)

        if not date_col or date_col not in df_full.columns or not self.start_date or not self.end_date:
            return df_full, pd.DataFrame()
        
        df_full[date_col] = pd.to_datetime(df_full[date_col]) # Garante que a coluna é do tipo datetime

        # Filtra período atual
        df_current = df_full[df_full[date_col].between(self.start_date, self.end_date)]

        # Calcula e filtra período anterior
        period_duration = self.end_date - self.start_date
        prev_end_date = self.start_date - pd.Timedelta(days=1)
        prev_start_date = prev_end_date - period_duration
        df_previous = df_full[df_full[date_col].between(prev_start_date, prev_end_date)]

        return df_current, df_previous

    def load_full_unfiltered_table(self, name: str) -> pd.DataFrame:
        """Carrega uma tabela completa, ignorando qualquer filtro de data."""
        table_name = self._map_name_to_table(name)
        if not table_name: return pd.DataFrame()
        conn = self._get_db_connection()
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        finally:
            conn.close()
        return df
    
    def get_date_range(self) -> tuple[pd.Timestamp | None, pd.Timestamp | None]:
        """Busca a data mínima e máxima na tabela de finanças para definir o calendário."""
        df_fin = self.load_full_unfiltered_table("Financas")
        if df_fin.empty or 'Data' not in df_fin.columns:
            return None, None
            
        valid_dates = pd.to_datetime(df_fin['Data'], errors='coerce').dropna()
        if valid_dates.empty:
            return None, None
            
        return valid_dates.min(), valid_dates.max()