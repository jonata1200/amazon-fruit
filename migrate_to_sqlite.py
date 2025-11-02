# migrate_to_sqlite.py

import os
import sys
import sqlite3
from typing import Optional, Dict, List

import pandas as pd

# ---------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------

EXCEL_FILE_CANDIDATES = [
    "amazon_fruit_dados.xlsx",
    "assets/amazon_fruit_dados.xlsx",
    "amazon-fruit.xlsx",
    "assets/amazon-fruit.xlsx",
]

DB_FILE = "amazon_fruit.db"

SHEET_TO_TABLE: Dict[str, str] = {
    "Estoque": "Estoque",
    "Fornecedores": "Fornecedores",
    "Publico_Alvo": "Publico_Alvo",
    "Financas": "Financas",
    "Recursos_Humanos": "Recursos_Humanos",
}

# ---------------------------------------------------------------------
# Schema (ajustado para bater com o Excel gerado)
# ---------------------------------------------------------------------

CREATE_STATEMENTS: Dict[str, str] = {
    "Estoque": """
        CREATE TABLE IF NOT EXISTS Estoque (
            ID_Produto TEXT PRIMARY KEY NOT NULL,
            Nome_Produto TEXT NOT NULL,
            Categoria TEXT,
            ID_Fornecedor TEXT,
            Quantidade_Estoque INTEGER DEFAULT 0,
            Preco_Custo REAL DEFAULT 0.0,
            Preco_Venda REAL DEFAULT 0.0,
            Data_Validade TEXT,
            Nivel_Minimo_Estoque INTEGER DEFAULT 0
        );
    """,
    "Fornecedores": """
        CREATE TABLE IF NOT EXISTS Fornecedores (
            ID_Fornecedor TEXT PRIMARY KEY NOT NULL,
            Nome_Fornecedor TEXT NOT NULL,
            CNPJ TEXT,
            Contato TEXT,
            Telefone TEXT,
            Email TEXT,
            Endereco TEXT,
            Cidade TEXT,
            Estado TEXT,
            CEP TEXT,
            Avaliacao INTEGER,
            Data_Ultima_Compra TEXT,
            Produtos_Fornecidos TEXT
        );
    """,
    "Publico_Alvo": """
        CREATE TABLE IF NOT EXISTS Publico_Alvo (
            ID_Cliente TEXT PRIMARY KEY NOT NULL,
            Nome TEXT NOT NULL,
            Genero TEXT,
            Idade INTEGER,
            Localizacao TEXT,
            Preferencias TEXT,
            Frequencia_Compra_Mensal INTEGER,
            Gasto_Medio REAL
        );
    """,
    "Financas": """
        CREATE TABLE IF NOT EXISTS Financas (
            ID_Lancamento INTEGER PRIMARY KEY AUTOINCREMENT,
            Data TEXT NOT NULL,
            Tipo TEXT NOT NULL,
            Categoria TEXT,
            Descricao TEXT,
            Valor REAL NOT NULL,
            Metodo_Pagamento TEXT,
            Centro_Custo TEXT,
            Pedido_Referencia TEXT
        );
    """,
    "Recursos_Humanos": """
        CREATE TABLE IF NOT EXISTS Recursos_Humanos (
            ID_Funcionario TEXT PRIMARY KEY NOT NULL,
            Nome TEXT NOT NULL,
            Cargo TEXT,
            Departamento TEXT,
            Data_Contratacao TEXT,
            Regime TEXT,
            Salario REAL,
            Cidade TEXT,
            Estado TEXT,
            Email TEXT
        );
    """,
}

# Coluna de data "principal" usada por alguns recursos do app (se necessário)
TABLE_DATE_COL = {
    "Financas": "Data",
    "Fornecedores": "Data_Ultima_Compra",
    "Recursos_Humanos": "Data_Contratacao",
    # "Estoque": "Data_Validade",  # só se precisar usar como "evento"
}

# ---------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------

def log(msg: str):
    print(msg, flush=True)

def find_excel() -> Optional[str]:
    for path in EXCEL_FILE_CANDIDATES:
        if os.path.exists(path):
            return path
    return None

def get_conn(db_path: str) -> sqlite3.Connection:
    return sqlite3.connect(db_path)

def get_table_columns(conn: sqlite3.Connection, table: str) -> List[str]:
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table})")
    return [row[1] for row in cur.fetchall()]

def filter_df_to_table(df: pd.DataFrame, conn: sqlite3.Connection, table: str) -> pd.DataFrame:
    cols_db = set(get_table_columns(conn, table))
    keep = [c for c in df.columns if c in cols_db]
    if not keep:
        raise ValueError(f"Nenhuma coluna da planilha bate com a tabela '{table}'. Colunas da planilha: {list(df.columns)} / Tabela possui: {list(cols_db)}")
    return df[keep]

def normalize_date_series(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, errors="coerce").dt.strftime("%Y-%m-%d")

def to_float_series(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce").astype(float)

def to_int_series(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce").fillna(0).astype(int)

# ---------------------------------------------------------------------
# Preparadores por tabela
# ---------------------------------------------------------------------

def prep_estoque(df: pd.DataFrame) -> pd.DataFrame:
    if "Quantidade_Estoque" in df.columns:
        df["Quantidade_Estoque"] = to_int_series(df["Quantidade_Estoque"])
    if "Preco_Custo" in df.columns:
        df["Preco_Custo"] = to_float_series(df["Preco_Custo"])
    if "Preco_Venda" in df.columns:
        df["Preco_Venda"] = to_float_series(df["Preco_Venda"])
    if "Data_Validade" in df.columns:
        df["Data_Validade"] = normalize_date_series(df["Data_Validade"])
    return df

def prep_fornecedores(df: pd.DataFrame) -> pd.DataFrame:
    if "Avaliacao" in df.columns:
        df["Avaliacao"] = to_int_series(df["Avaliacao"])
    if "Data_Ultima_Compra" in df.columns:
        df["Data_Ultima_Compra"] = normalize_date_series(df["Data_Ultima_Compra"])
    # Campos de texto
    for col in ["CNPJ","Contato","Telefone","Email","Endereco","Cidade","Estado","CEP","Produtos_Fornecidos","Nome_Fornecedor"]:
        if col in df.columns:
            df[col] = df[col].astype(str)
    return df

def prep_publico(df: pd.DataFrame) -> pd.DataFrame:
    if "Idade" in df.columns:
        df["Idade"] = to_int_series(df["Idade"])
    if "Frequencia_Compra_Mensal" in df.columns:
        df["Frequencia_Compra_Mensal"] = to_int_series(df["Frequencia_Compra_Mensal"])
    if "Gasto_Medio" in df.columns:
        df["Gasto_Medio"] = to_float_series(df["Gasto_Medio"])
    for col in ["Genero","Localizacao","Preferencias","Nome"]:
        if col in df.columns:
            df[col] = df[col].astype(str)
    return df

def prep_financas(df: pd.DataFrame) -> pd.DataFrame:
    # Deixar o SQLite autoincrementar
    if "ID_Lancamento" in df.columns:
        df = df.drop(columns=["ID_Lancamento"])

    if "Data" in df.columns:
        df["Data"] = normalize_date_series(df["Data"])
    if "Valor" in df.columns:
        df["Valor"] = to_float_series(df["Valor"])
    for col in ["Tipo","Categoria","Descricao","Metodo_Pagamento","Centro_Custo","Pedido_Referencia"]:
        if col in df.columns:
            df[col] = df[col].astype(str)
    return df

def prep_rh(df: pd.DataFrame) -> pd.DataFrame:
    if "Data_Contratacao" in df.columns:
        df["Data_Contratacao"] = normalize_date_series(df["Data_Contratacao"])
    if "Salario" in df.columns:
        df["Salario"] = to_float_series(df["Salario"])
    for col in ["Nome","Cargo","Departamento","Regime","Cidade","Estado","Email"]:
        if col in df.columns:
            df[col] = df[col].astype(str)
    return df

PREP_BY_TABLE = {
    "Estoque": prep_estoque,
    "Fornecedores": prep_fornecedores,
    "Publico_Alvo": prep_publico,
    "Financas": prep_financas,
    "Recursos_Humanos": prep_rh,
}

# ---------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------

def create_schema(conn: sqlite3.Connection):
    log("\n[INFO] Criando schema do banco de dados...")
    cur = conn.cursor()
    for tbl, ddl in CREATE_STATEMENTS.items():
        log(f"  - Preparando tabela '{tbl}'...")
        cur.execute(ddl)
    conn.commit()
    log("[OK] Schema criado com sucesso.\n")

def load_sheet_to_table(xls_path: str, sheet_name: str, table_name: str, conn: sqlite3.Connection):
    log(f"[INFO] Processando planilha '{sheet_name}' para a tabela '{table_name}'...")
    df = pd.read_excel(xls_path, sheet_name=sheet_name, dtype=str)

    # Converte tipos específicos por tabela
    prep_fn = PREP_BY_TABLE.get(table_name)
    if prep_fn:
        df = prep_fn(df)

    # Filtra para colunas existentes na tabela
    df = filter_df_to_table(df, conn, table_name)

    # Inserção
    df.to_sql(table_name, conn, if_exists="append", index=False)
    log(f"  [OK] Tabela '{table_name}' populada com {len(df)} linhas.")

def main():
    excel_path = find_excel()
    if not excel_path:
        log("[ERRO] Nenhum arquivo Excel encontrado. Ajuste EXCEL_FILE_CANDIDATES ou coloque o arquivo na raiz.")
        sys.exit(1)

    log(f"[INFO] Usando Excel: {excel_path}\n")

    # Recria o banco (se quiser manter o anterior, remova o bloco abaixo)
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    try:
        with get_conn(DB_FILE) as conn:
            create_schema(conn)

            for sheet, table in SHEET_TO_TABLE.items():
                try:
                    load_sheet_to_table(excel_path, sheet, table, conn)
                except Exception as e:
                    log(f"\n[ERRO] Falha ao processar '{sheet}' -> '{table}': {e}")
                    raise

    except Exception as e:
        log(f"\n[ERRO CRÍTICO] A migração falhou: {e}")
        sys.exit(1)

    log("\n[OK] Migração concluída com sucesso.")

if __name__ == "__main__":
    main()