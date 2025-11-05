# modules/analysis/suppliers_analysis.py
import pandas as pd
from modules.utils.data_handler import DataRepository

# A instância do repo pode ser mantida se outras partes do programa a usarem.
repo = DataRepository()

def ranking_fornecedores(df: pd.DataFrame, top: int = 10) -> pd.DataFrame:
    if df is None or df.empty or 'Avaliacao' not in df.columns:
        return pd.DataFrame(columns=["ID_Fornecedor", "Nome_Fornecedor", "Avaliacao", "Cidade", "Estado", "Produtos_Fornecidos"])
    return df.sort_values("Avaliacao", ascending=False).head(top)[["ID_Fornecedor","Nome_Fornecedor","Avaliacao","Cidade","Estado","Produtos_Fornecidos"]]

def analyze_suppliers_kpis(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {'total_suppliers': 0, 'avg_rating': float('nan')}
    total_suppliers = len(df)
    avg_rating = pd.to_numeric(df.get('Avaliacao'), errors='coerce').mean()
    return {'total_suppliers': total_suppliers, 'avg_rating': avg_rating}

def get_product_types_distribution(df: pd.DataFrame) -> pd.Series:
    if df is None or df.empty or 'Produtos_Fornecidos' not in df.columns:
        return pd.Series(dtype='object')
    all_types = []
    for item in df['Produtos_Fornecidos'].dropna().astype(str):
        all_types.extend([t.strip() for t in item.split(',') if t.strip()])
    if not all_types:
        return pd.Series(dtype='object')
    return pd.Series(all_types).value_counts()

# --- NOVA FUNÇÃO ADICIONADA AQUI ---
def create_supplier_product_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria uma matriz binária (0 ou 1) de Fornecedores x Produtos.
    O valor 1 indica que o fornecedor oferece o produto.
    """
    if df is None or df.empty or not {'Nome_Fornecedor', 'Produtos_Fornecidos'}.issubset(df.columns):
        return pd.DataFrame()

    # 1. Copia o DataFrame e remove linhas onde os produtos não são especificados
    df_exp = df[['Nome_Fornecedor', 'Produtos_Fornecidos']].dropna()

    # 2. Transforma a string de produtos "A, B, C" em uma lista de produtos ['A', 'B', 'C']
    df_exp['Produtos_Fornecidos'] = df_exp['Produtos_Fornecidos'].str.split(',')

    # 3. "Explode" o DataFrame, criando uma nova linha para cada produto de cada fornecedor
    df_exp = df_exp.explode('Produtos_Fornecidos')

    # 4. Remove espaços em branco extras dos nomes dos produtos
    df_exp['Produtos_Fornecidos'] = df_exp['Produtos_Fornecidos'].str.strip()

    # 5. Cria a tabela cruzada (matriz), que é a base do nosso heatmap
    matrix = pd.crosstab(df_exp['Nome_Fornecedor'], df_exp['Produtos_Fornecidos'])
    
    return matrix