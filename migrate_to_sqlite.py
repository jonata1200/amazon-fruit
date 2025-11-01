# migrate_to_sqlite.py

import os
import sys
import sqlite3
from typing import Dict, Tuple, Optional

import pandas as pd


# ---------------------------------------------------------------------
# Configurações e utilitários
# ---------------------------------------------------------------------

EXCEL_FILE_CANDIDATES = [
    "amazon_fruit_dados.xlsx",
    "assets/amazon_fruit_dados.xlsx",
]
DB_FILE = "amazon_fruit.db"

SHEET_TO_TABLE = {
    "Estoque": "Estoque",
    "Fornecedores": "Fornecedores",
    "Publico_Alvo": "Publico_Alvo",
    "Financas": "Financas",
    "Recursos_Humanos": "Recursos_Humanos",
}

# Coerção de tipos por tabela (somente se a coluna existir no df)
# Obs.: Mantemos todo o processo tolerante a esquemas parcialmente preenchidos.
TYPE_RULES: Dict[str, Dict[str, str]] = {
    "Estoque": {
        "ID_Produto": "str",
        "Nome_Produto": "str",
        "Categoria": "str",
        "ID_Fornecedor": "str",
        "Quantidade_Estoque": "int",
        "Preco_Custo": "float",
        "Preco_Venda": "float",
        "Data_Validade": "date",
        "Nivel_Minimo_Estoque": "int",
    },
    "Fornecedores": {
        "ID_Fornecedor": "str",
        "Nome_Fornecedor": "str",
        "Contato": "str",
        "Telefone": "str",
        "Email": "str",
        "Cidade": "str",
        "Estado": "str",
        "Avaliacao": "int",
    },
    "Publico_Alvo": {
        "ID_Cliente": "str",
        "Nome": "str",
        "Idade": "int",
        "Genero": "str",
        "Cidade": "str",
        "Estado": "str",
        "Frequencia_Compra": "int",
        "Ticket_Medio": "float",
    },
    "Financas": {
        "ID_Lancamento": "str",
        "Data": "date",
        "Categoria": "str",
        "Descricao": "str",
        "Valor": "float",
    },
    "Recursos_Humanos": {
        "ID_Funcionario": "str",
        "Nome_Funcionario": "str",
        "Cargo": "str",
        "Salario": "float",
        "Data_Contratacao": "date",
        "Status": "str",
    },
}


def find_excel_file() -> Optional[str]:
    for path in EXCEL_FILE_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Remove espaços nas extremidades e troca espaços internos por underscore
    df = df.copy()
    df.columns = [str(c).strip().replace(" ", "_") for c in df.columns]
    return df


def coerce_types(df: pd.DataFrame, table: str) -> pd.DataFrame:
    """
    Aplica coerção de tipos conforme TYPE_RULES[table], quando a coluna existir.
    - str: to string
    - int: para inteiro (coage nulos para 0)
    - float: para float (nulos viram 0.0)
    - date: tenta parse para datetime.date; mantém string ISO se não parsear
    """
    rules = TYPE_RULES.get(table, {})
    if not rules:
        return df

    df = df.copy()
    for col, kind in rules.items():
        if col not in df.columns:
            continue
        if kind == "str":
            df[col] = df[col].astype(str)
        elif kind == "int":
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype("int64")
        elif kind == "float":
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0).astype("float64")
        elif kind == "date":
            # Tenta parse para datetime; exportaremos como texto ISO (YYYY-MM-DD)
            parsed = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
            df[col] = parsed.dt.date.astype(str)  # mantém 'YYYY-MM-DD' ou 'NaT'→'NaT'
        else:
            # desconhecido → não faz nada
            pass
    return df


def trim_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove linhas completamente vazias (todas colunas NaN/''/None).
    """
    if df.empty:
        return df
    # Considera vazio strings vazias; substitui por NaN para a verificação
    df = df.replace(r"^\s*$", pd.NA, regex=True)
    return df.dropna(how="all").reset_index(drop=True)


def read_sheet(xls: pd.ExcelFile, sheet_name: str) -> pd.DataFrame:
    try:
        df = xls.parse(sheet_name)
    except ValueError:
        # Tenta variações comuns de nome
        candidates = [sheet_name, sheet_name.replace("_", " "), sheet_name.lower(), sheet_name.upper()]
        found = None
        for s in xls.sheet_names:
            if s in candidates:
                found = s
                break
        if not found:
            # Procura por aproximação simples
            for s in xls.sheet_names:
                if s.replace(" ", "_").lower() == sheet_name.lower():
                    found = s
                    break
        if not found:
            raise
        df = xls.parse(found)

    df = normalize_columns(df)
    df = trim_empty_rows(df)
    return df


def write_table(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str) -> Tuple[int, int]:
    """
    Escreve df na tabela (replace). Retorna (rows_before, rows_after) para log.
    """
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT COUNT(1) FROM {table_name}")
        before = cur.fetchone()[0]
    except sqlite3.Error:
        before = 0

    # Escreve com replace
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    cur.execute(f"SELECT COUNT(1) FROM {table_name}")
    after = cur.fetchone()[0]
    return before, after


# ---------------------------------------------------------------------
# Fluxo principal
# ---------------------------------------------------------------------

def migrate_data() -> int:
    excel_file = find_excel_file()
    if not excel_file:
        print("Erro: Não encontrei 'amazon_fruit_dados.xlsx' na raiz nem em 'assets/'.")
        return 2

    print(f"[OK] Usando Excel: {excel_file}")
    try:
        xls = pd.ExcelFile(excel_file)
    except Exception as e:
        print(f"Erro ao abrir o Excel: {e}")
        return 3

    # Abre conexão SQLite
    try:
        conn = sqlite3.connect(DB_FILE)
    except Exception as e:
        print(f"Erro ao abrir/criar banco '{DB_FILE}': {e}")
        return 4

    try:
        for sheet, table in SHEET_TO_TABLE.items():
            if sheet not in xls.sheet_names:
                # Tentativa permissiva: ler via read_sheet (que já trata variações)
                pass
            try:
                df = read_sheet(xls, sheet)
            except Exception as e:
                print(f"[AVISO] Planilha '{sheet}' não encontrada ou erro ao ler: {e}")
                continue

            # Coerção de tipos conforme tabela
            df = coerce_types(df, table)

            if df.empty:
                print(f"[AVISO] Planilha '{sheet}' está vazia após limpeza. Ignorando.")
                continue

            # Escreve no SQLite
            before, after = write_table(conn, df, table)
            print(f"[OK] Tabela '{table}' atualizada: {before} → {after} linhas.")

        conn.commit()
        print(f"[FINALIZADO] Migração concluída com sucesso em '{DB_FILE}'.")
        return 0
    except Exception as e:
        print(f"Erro na migração: {e}")
        return 5
    finally:
        conn.close()


if __name__ == "__main__":
    # Uso: python migrate_to_sqlite.py
    code = migrate_data()
    # Retorna código de saída útil para CI/scripts
    sys.exit(code)