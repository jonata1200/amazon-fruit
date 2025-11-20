# backend/app/services/analysis/inventory_analysis.py

import pandas as pd
from typing import Optional

def estoque_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna estoque total agrupado por mês.
    
    Args:
        df: DataFrame com dados de estoque
        
    Returns:
        DataFrame com quantidade total por mês
    """
    if df is None or df.empty or "Data_Snapshot" not in df.columns:
        return pd.DataFrame()
    df_copy = df.copy()
    df_copy["AnoMes"] = pd.to_datetime(df_copy["Data_Snapshot"], errors='coerce').dt.to_period("M").astype(str)
    return (df_copy.groupby(["AnoMes"], as_index=False)["Quantidade_Estoque"]
              .sum().rename(columns={"Quantidade_Estoque": "Qtd_Total"}))

def rupturas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna produtos com estoque abaixo do nível mínimo.
    
    Args:
        df: DataFrame com dados de estoque
        
    Returns:
        DataFrame com produtos em ruptura
    """
    if df is None or df.empty:
        return pd.DataFrame()
    df_copy = df.copy()
    df_copy['Data_Snapshot'] = pd.to_datetime(df_copy['Data_Snapshot'], errors='coerce')
    ult = df_copy.sort_values("Data_Snapshot").groupby("ID_Produto").tail(1)
    return ult[ult["Quantidade_Estoque"] < ult["Nivel_Minimo_Estoque"]]

def _get_change(current, previous):
    """Calcula a variação percentual entre dois valores"""
    if previous is None or pd.isna(previous) or previous == 0:
        return None
    return (current - previous) / previous

def analyze_inventory_kpis(df_current: pd.DataFrame, df_previous: Optional[pd.DataFrame] = None) -> dict:
    """
    Analisa e retorna os KPIs de estoque para o período atual e a variação.
    
    Args:
        df_current: DataFrame com dados do período atual
        df_previous: DataFrame com dados do período anterior (opcional)
        
    Returns:
        Dicionário com KPIs de estoque e variações
    """
    def _calculate(df: pd.DataFrame):
        if df is None or df.empty:
            return {'unique_products': 0, 'total_value': 0.0, 'low_stock_count': 0}
        
        unique_products = df['ID_Produto'].nunique() if 'ID_Produto' in df.columns else len(df)
        
        total_value = 0.0
        if {'Quantidade_Estoque', 'Preco_Custo'}.issubset(df.columns):
            q = pd.to_numeric(df['Quantidade_Estoque'], errors='coerce').fillna(0)
            c = pd.to_numeric(df['Preco_Custo'], errors='coerce').fillna(0.0)
            total_value = float((q * c).sum())
            
        low_stock_count = 0
        if {'Quantidade_Estoque', 'Nivel_Minimo_Estoque'}.issubset(df.columns):
            q2 = pd.to_numeric(df['Quantidade_Estoque'], errors='coerce')
            n2 = pd.to_numeric(df['Nivel_Minimo_Estoque'], errors='coerce')
            low_stock_count = int((q2 <= n2).sum())
            
        return {
            'unique_products': unique_products,
            'total_value': total_value,
            'low_stock_count': low_stock_count
        }

    summary_current = _calculate(df_current)
    summary_previous = _calculate(df_previous)

    summary_current['total_value_change'] = _get_change(summary_current['total_value'], summary_previous['total_value'])
    summary_current['low_stock_count_change'] = _get_change(summary_current['low_stock_count'], summary_previous['low_stock_count'])
    
    return summary_current

def get_low_stock_items(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Retorna um DataFrame com os itens de estoque baixo, considerando apenas
    o registro mais recente de cada produto no período fornecido.
    
    Args:
        df: DataFrame com dados de estoque
        top_n: Número de itens a retornar
        
    Returns:
        DataFrame com produtos de estoque baixo ordenados por gap
    """
    req = {'Produto', 'ID_Produto', 'Quantidade_Estoque', 'Nivel_Minimo_Estoque', 'Data_Snapshot'}
    if df is None or df.empty or not req.issubset(df.columns):
        return pd.DataFrame()

    df_latest = df.copy()
    df_latest['Data_Snapshot'] = pd.to_datetime(df_latest['Data_Snapshot'], errors='coerce')
    df_latest.dropna(subset=['Data_Snapshot'], inplace=True)

    df_latest = df_latest.sort_values('Data_Snapshot').groupby('ID_Produto').tail(1)

    df_latest['gap'] = pd.to_numeric(df_latest['Nivel_Minimo_Estoque'], errors='coerce') - \
                       pd.to_numeric(df_latest['Quantidade_Estoque'], errors='coerce')
    
    return df_latest[df_latest['gap'] > 0].sort_values('gap', ascending=False).head(top_n)

