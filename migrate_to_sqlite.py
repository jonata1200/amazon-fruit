# migrate_to_sqlite.py

import pandas as pd
import sqlite3
import os

EXCEL_FILE = 'amazon_fruit_dados.xlsx'
DB_FILE = 'amazon_fruit.db'

def migrate_data():
    """
    Lê todas as abas do arquivo Excel e as salva como tabelas em um banco de dados SQLite.
    Este script deve ser executado apenas uma vez.
    """
    if not os.path.exists(EXCEL_FILE):
        print(f"Erro: Arquivo '{EXCEL_FILE}' não encontrado.")
        return

    print("Iniciando a migração de dados do Excel para o SQLite...")

    try:
        # Conecta ao banco de dados (cria o arquivo se não existir)
        conn = sqlite3.connect(DB_FILE)
        
        # Lê todas as abas do Excel de uma vez
        all_sheets = pd.read_excel(EXCEL_FILE, sheet_name=None)
        
        # Itera sobre cada aba (DataFrame) e a salva no banco de dados
        for sheet_name, df in all_sheets.items():
            # Substitui caracteres especiais no nome da aba para criar um nome de tabela válido
            table_name = sheet_name.replace(' ', '_')
            print(f"  - Processando tabela: '{table_name}'...")
            
            # Usa a função to_sql do pandas para criar a tabela e inserir os dados
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        conn.close()
        print("\nMigração concluída com sucesso!")
        print(f"Os dados agora estão no arquivo '{DB_FILE}'.")
        print("Você pode apagar este script ('migrate_to_sqlite.py') após a execução.")

    except Exception as e:
        print(f"Ocorreu um erro durante a migração: {e}")

if __name__ == "__main__":
    migrate_data()