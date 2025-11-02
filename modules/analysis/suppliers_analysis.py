# modules/analysis/suppliers_analysis.py
import pandas as pd
import math

def analyze_suppliers_kpis(df: pd.DataFrame) -> dict:
    """
    Analisa e retorna os KPIs de fornecedores.

    Returns:
        Um dicionário com 'total_suppliers' e 'avg_rating'.
    """
    if df is None or df.empty:
        return {'total_suppliers': 0, 'avg_rating': float('nan')}
    
    total_suppliers = len(df)
    
    avg_rating = float('nan')
    if 'Avaliacao' in df.columns:
        avg_rating = pd.to_numeric(df['Avaliacao'], errors='coerce').mean()
        
    return {
        'total_suppliers': total_suppliers,
        'avg_rating': avg_rating
    }

def get_product_types_distribution(df: pd.DataFrame) -> pd.Series:
    """
    Extrai e conta todos os tipos de produtos fornecidos.

    Returns:
        Uma pd.Series com a contagem de cada tipo de produto.
    """
    if df is None or df.empty or 'Produtos_Fornecidos' not in df.columns:
        return pd.Series(dtype='object')
        
    all_types = []
    # Itera sobre cada célula, divide por vírgula e adiciona a uma lista única
    for item in df['Produtos_Fornecidos'].dropna().astype(str):
        all_types.extend([t.strip() for t in item.split(',') if t.strip()])
    
    if not all_types:
        return pd.Series(dtype='object')
        
    return pd.Series(all_types).value_counts()