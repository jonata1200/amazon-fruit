# scripts/check_excel_columns.py

from pathlib import Path
import pandas as pd

# Define o caminho para a pasta de dados
project_root = Path(__file__).resolve().parents[1]
ESTOQUE_DIR = project_root / 'data' / 'estoque'

def check_stock_columns():
    """
    Itera sobre todos os arquivos 'estoque.xlsx' e imprime os nomes das colunas
    de cada aba para diagnosticar inconsistências.
    """
    print("--- INICIANDO DIAGNÓSTICO DAS COLUNAS DE ESTOQUE ---")

    if not ESTOQUE_DIR.exists():
        print(f"ERRO: Diretório de estoque não encontrado em: {ESTOQUE_DIR}")
        return

    stock_files = list(ESTOQUE_DIR.glob('*/estoque.xlsx'))
    
    if not stock_files:
        print("Nenhum arquivo 'estoque.xlsx' encontrado para verificar.")
        return

    print(f"Encontrados {len(stock_files)} arquivos para analisar.\n")

    for file_path in stock_files:
        print(f"=====================================================")
        print(f"Analisando arquivo: {file_path.relative_to(project_root)}")
        print(f"=====================================================")
        
        try:
            xls = pd.ExcelFile(file_path, engine='openpyxl')
            
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                # Imprime a lista de colunas para esta aba específica
                print(f"  - Aba: '{sheet_name}' -> Colunas: {list(df.columns)}")
            
            print("\n")

        except Exception as e:
            print(f"  --> OCORREU UM ERRO ao ler o arquivo {file_path.name}: {e}\n")

    print("--- DIAGNÓSTICO CONCLUÍDO ---")

if __name__ == '__main__':
    check_stock_columns()