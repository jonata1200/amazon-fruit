# migrate_to_sqlite.py

import os
import sys
import sqlite3
from typing import Optional

import pandas as pd


# ---------------------------------------------------------------------
# Configurações e Mapeamentos
# ---------------------------------------------------------------------

EXCEL_FILE_CANDIDATES = ["amazon_fruit_dados.xlsx", "assets/amazon_fruit_dados.xlsx"]
DB_FILE = "amazon_fruit.db"

SHEET_TO_TABLE = {
    "Estoque": "Estoque",
    "Fornecedores": "Fornecedores",
    "Publico_Alvo": "Publico_Alvo",
    "Financas": "Financas",
    "Recursos_Humanos": "Recursos_Humanos",
}

# --- NOVO: Definição do Schema do Banco de Dados (DDL) ---
# Aqui definimos a estrutura exata de cada tabela, com chaves primárias e restrições.
SCHEMAS = {
    "Estoque": """
        CREATE TABLE Estoque (
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
        CREATE TABLE Fornecedores (
            ID_Fornecedor TEXT PRIMARY KEY NOT NULL,
            Nome_Fornecedor TEXT NOT NULL,
            Contato TEXT,
            Telefone TEXT,
            Email TEXT,
            Cidade TEXT,
            Estado TEXT,
            Avaliacao INTEGER,
            Data_Ultima_Compra TEXT
        );
    """,
    "Publico_Alvo": """
        CREATE TABLE Publico_Alvo (
            ID_Cliente TEXT PRIMARY KEY NOT NULL,
            Nome TEXT NOT NULL,
            Idade INTEGER,
            Genero TEXT,
            Localizacao TEXT,
            Gasto_Medio REAL,
            Frequencia_Compra_Mensal INTEGER
        );
    """,
    "Financas": """
        CREATE TABLE Financas (
            ID_Lancamento INTEGER PRIMARY KEY AUTOINCREMENT,
            Data TEXT NOT NULL,
            Tipo TEXT NOT NULL,
            Categoria TEXT,
            Descricao TEXT,
            Valor REAL NOT NULL
        );
    """,
    "Recursos_Humanos": """
        CREATE TABLE Recursos_Humanos (
            ID_Funcionario TEXT PRIMARY KEY NOT NULL,
            Nome_Funcionario TEXT NOT NULL,
            Cargo TEXT,
            Salario REAL,
            Data_Contratacao TEXT,
            Status TEXT
        );
    """,
}

# ---------------------------------------------------------------------
# Funções Utilitárias (com melhorias)
# ---------------------------------------------------------------------

def find_excel_file() -> Optional[str]:
    for path in EXCEL_FILE_CANDIDATES:
        if os.path.exists(path):
            return path
    return None

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().replace(" ", "_") for c in df.columns]
    return df

def coerce_types(df: pd.DataFrame, table: str) -> pd.DataFrame:
    """
    Aplica coerção de tipos e AVISA sobre dados que não puderam ser convertidos.
    """
    df = df.copy()
    # Mapeamento simples para facilitar o loop
    type_map = {
        'int': ('integer', 0),
        'float': ('float', 0.0),
        'str': ('string', ''),
        'date': ('datetime', None)
    }

    # As regras de tipo agora são usadas para validação
    rules = {
        "Estoque": {"Quantidade_Estoque": "int", "Preco_Custo": "float", "Preco_Venda": "float", "Data_Validade": "date", "Nivel_Minimo_Estoque": "int"},
        "Fornecedores": {"Avaliacao": "int", "Data_Ultima_Compra": "date"},
        "Publico_Alvo": {"Idade": "int", "Gasto_Medio": "float", "Frequencia_Compra_Mensal": "int"},
        "Financas": {"Data": "date", "Valor": "float"},
        "Recursos_Humanos": {"Salario": "float", "Data_Contratacao": "date"},
    }
    
    table_rules = rules.get(table, {})
    for col, kind in table_rules.items():
        if col not in df.columns:
            continue
        
        original_series = df[col]
        
        # --- LÓGICA ATUALIZADA COM AVISOS ---
        if kind in ['int', 'float']:
            numeric_series = pd.to_numeric(original_series, errors='coerce')
            invalid_rows = original_series.notna() & numeric_series.isna()
            if invalid_rows.any():
                print(f"  [AVISO] Dados inválidos na Tabela '{table}', Coluna '{col}'. As seguintes linhas serão ignoradas (definidas como 0):")
                print(df.loc[invalid_rows, [col]].to_string(index=False, header=False))
            
            fill_value = 0 if kind == 'int' else 0.0
            df[col] = numeric_series.fillna(fill_value).astype(kind)

        elif kind == 'date':
            parsed = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
            invalid_rows = original_series.notna() & parsed.isna()
            if invalid_rows.any():
                 print(f"  [AVISO] Datas inválidas na Tabela '{table}', Coluna '{col}'. As seguintes linhas serão ignoradas (definidas como Nulas):")
                 print(df.loc[invalid_rows, [col]].to_string(index=False, header=False))
            
            # Converte para string no formato YYYY-MM-DD, valores inválidos viram 'NaT'
            df[col] = parsed.dt.strftime('%Y-%m-%d').replace({pd.NaT: None})
            
    return df

def trim_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return df
    df = df.replace(r"^\s*$", pd.NA, regex=True)
    return df.dropna(how="all").reset_index(drop=True)

def read_sheet(xls: pd.ExcelFile, sheet_name: str) -> pd.DataFrame:
    df = xls.parse(sheet_name)
    df = normalize_columns(df)
    df = trim_empty_rows(df)
    return df

# --- NOVA FUNÇÃO ---
def create_tables(conn: sqlite3.Connection):
    """Cria todas as tabelas no banco de dados a partir dos schemas definidos."""
    cur = conn.cursor()
    print("\n[INFO] Criando schema do banco de dados...")
    for table_name, ddl_query in SCHEMAS.items():
        print(f"  - Preparando tabela '{table_name}'...")
        cur.execute(f"DROP TABLE IF EXISTS {table_name};")
        cur.execute(ddl_query)
    conn.commit()
    print("[OK] Schema criado com sucesso.\n")

def write_table(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str) -> int:
    """Escreve o DataFrame na tabela (append). Retorna o número de linhas inseridas."""
    # --- LÓGICA ATUALIZADA para usar 'append' ---
    df.to_sql(table_name, conn, if_exists="append", index=False)
    return len(df)

# ---------------------------------------------------------------------
# Fluxo Principal da Migração
# ---------------------------------------------------------------------

def migrate_data() -> int:
    excel_file = find_excel_file()
    if not excel_file:
        print("Erro: Não encontrei 'amazon_fruit_dados.xlsx'.")
        return 2

    print(f"[INFO] Usando Excel: {excel_file}")
    try:
        xls = pd.ExcelFile(excel_file)
    except Exception as e:
        print(f"Erro ao abrir o Excel: {e}")
        return 3

    try:
        conn = sqlite3.connect(DB_FILE)
        # --- ETAPA ADICIONADA: Cria as tabelas antes de inserir os dados ---
        create_tables(conn)
        
        for sheet, table in SHEET_TO_TABLE.items():
            if sheet not in xls.sheet_names:
                print(f"[AVISO] Planilha '{sheet}' não encontrada no Excel. Ignorando.")
                continue

            print(f"[INFO] Processando planilha '{sheet}' para a tabela '{table}'...")
            df = read_sheet(xls, sheet)
            df = coerce_types(df, table)

            if df.empty:
                print(f"  [AVISO] Planilha '{sheet}' está vazia após limpeza. Nenhuma linha inserida.")
                continue

            # Escreve no SQLite
            rows_added = write_table(conn, df, table)
            print(f"  [OK] Tabela '{table}' populada com {rows_added} linhas.")

        conn.commit()
        print(f"\n[FINALIZADO] Migração concluída com sucesso para o banco de dados '{DB_FILE}'.")
        return 0
    except Exception as e:
        print(f"\n[ERRO CRÍTICO] A migração falhou: {e}")
        return 5
    finally:
        if 'conn' in locals() and conn:
            conn.close()


if __name__ == "__main__":
    code = migrate_data()
    sys.exit(code)