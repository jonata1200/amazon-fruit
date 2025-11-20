# backend/app/services/analysis/financial_analysis.py

import pandas as pd
from typing import Optional

def _get_change(current, previous):
    """Calcula a variação percentual entre dois valores"""
    if previous is None or pd.isna(previous) or previous == 0:
        return None
    return (current - previous) / previous

def calculate_financial_summary(df_current: pd.DataFrame, df_previous: Optional[pd.DataFrame] = None) -> dict:
    """
    Calcula resumo financeiro (receita, despesa, lucro) e variações percentuais.
    
    Args:
        df_current: DataFrame com dados do período atual
        df_previous: DataFrame com dados do período anterior (opcional)
        
    Returns:
        Dicionário com receita, despesa, lucro e variações percentuais
    """
    def _calculate(df):
        if df is None or df.empty:
            return {'receita': 0.0, 'despesa': 0.0, 'lucro': 0.0}
        t = df['Tipo'].astype(str).str.lower()
        v = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        receita = float(v[t.str.contains('receita', case=False)].sum())
        despesa = float(v[t.str.contains('despesa', case=False)].sum())
        return {'receita': receita, 'despesa': despesa, 'lucro': receita - despesa}
    
    summary_current = _calculate(df_current)
    summary_previous = _calculate(df_previous)
    summary_current['receita_change'] = _get_change(summary_current['receita'], summary_previous['receita'])
    summary_current['despesa_change'] = _get_change(summary_current['despesa'], summary_previous['despesa'])
    summary_current['lucro_change'] = _get_change(summary_current['lucro'], summary_previous['lucro'])
    return summary_current

def get_expense_distribution(df: pd.DataFrame) -> pd.Series:
    """
    Retorna distribuição de despesas por categoria.
    
    Args:
        df: DataFrame com dados financeiros
        
    Returns:
        Series com despesas agrupadas por categoria
    """
    if df is None or df.empty or not {'Categoria', 'Tipo', 'Valor'}.issubset(df.columns):
        return pd.Series(dtype='float64')
    expenses_df = df[df['Tipo'].astype(str).str.lower() == 'despesa']
    return expenses_df.groupby('Categoria')['Valor'].sum().sort_values(ascending=False)

def get_revenue_distribution(df: pd.DataFrame, top_n: int = 5) -> pd.Series:
    """
    Retorna distribuição de receitas por categoria (top N).
    
    Args:
        df: DataFrame com dados financeiros
        top_n: Número de categorias a retornar
        
    Returns:
        Series com receitas agrupadas por categoria
    """
    if df is None or df.empty or not {'Categoria', 'Tipo', 'Valor'}.issubset(df.columns):
        return pd.Series(dtype='float64')
    revenue_df = df[df['Tipo'].astype(str).str.lower() == 'receita']
    return revenue_df.groupby('Categoria')['Valor'].sum().sort_values(ascending=False).head(top_n)

def get_top_selling_items(df_financas: pd.DataFrame, df_estoque: pd.DataFrame, top_n: int = 10) -> pd.Series:
    """
    Identifica os produtos mais vendidos a partir dos DADOS DE ESTOQUE.
    
    Args:
        df_financas: DataFrame de finanças (não usado, mantido para compatibilidade)
        df_estoque: DataFrame de estoque
        top_n: Número de produtos a retornar
        
    Returns:
        Series com faturamento por produto
    """
    if df_estoque is None or df_estoque.empty:
        return pd.Series(dtype='float64')

    required_cols = {'Produto', 'Quantidade_Vendida', 'Preco_Venda'}
    if not required_cols.issubset(df_estoque.columns):
        return pd.Series(dtype='float64')

    sales_df = df_estoque.copy()
    sales_df['Quantidade_Vendida'] = pd.to_numeric(sales_df['Quantidade_Vendida'], errors='coerce').fillna(0)
    sales_df['Preco_Venda'] = pd.to_numeric(sales_df['Preco_Venda'], errors='coerce').fillna(0)
    sales_df['Faturamento'] = sales_df['Quantidade_Vendida'] * sales_df['Preco_Venda']

    top_selling = sales_df.groupby('Produto')['Faturamento'].sum()
    
    return top_selling.sort_values(ascending=False).head(top_n)

def get_least_selling_items(df_financas: pd.DataFrame, df_estoque: pd.DataFrame, top_n: int = 10) -> pd.Series:
    """
    Identifica os produtos menos vendidos, incluindo aqueles que nunca foram vendidos.
    
    Args:
        df_financas: DataFrame de finanças (não usado, mantido para compatibilidade)
        df_estoque: DataFrame de estoque
        top_n: Número de produtos a retornar
        
    Returns:
        Series com faturamento por produto (menores valores primeiro)
    """
    if df_estoque is None or df_estoque.empty:
        return pd.Series(dtype='float64')

    if 'Produto' not in df_estoque.columns:
        return pd.Series(dtype='float64')

    all_products = df_estoque[['Produto']].drop_duplicates().set_index('Produto')

    sales_df = df_estoque.copy()
    sales_df['Quantidade_Vendida'] = pd.to_numeric(sales_df['Quantidade_Vendida'], errors='coerce').fillna(0)
    sales_df['Preco_Venda'] = pd.to_numeric(sales_df['Preco_Venda'], errors='coerce').fillna(0)
    sales_df['Faturamento'] = sales_df['Quantidade_Vendida'] * sales_df['Preco_Venda']

    sales_summary = sales_df.groupby('Produto')['Faturamento'].sum()

    combined = all_products.join(sales_summary)
    least_selling = combined.fillna(0).sort_values('Faturamento', ascending=True).head(top_n)

    return least_selling['Faturamento']

