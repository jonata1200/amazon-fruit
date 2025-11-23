# backend/app/services/charts/inventory_charts.py

import pandas as pd
import plotly.graph_objects as go
from typing import Dict

# Importar funções de análise
from ..analysis import financial_analysis, inventory_analysis

def create_top_selling_chart_data(df_fin: pd.DataFrame, df_estoque: pd.DataFrame, top_n: int = 10) -> Dict:
    """
    Cria dados para gráfico de Top N Produtos por Faturamento.
    
    Args:
        df_fin: DataFrame de finanças (não usado, mantido para compatibilidade)
        df_estoque: DataFrame de estoque
        top_n: Número de produtos a retornar
        
    Returns:
        Dicionário com estrutura Plotly
    """
    top_selling = financial_analysis.get_top_selling_items(df_fin, df_estoque, top_n=top_n)
    
    if top_selling.empty:
        return {"data": [], "layout": {}}
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top_selling.values,
        y=top_selling.index,
        orientation='h',
        marker_color='#2ECC71',
        name='Faturamento'
    ))
    
    fig.update_layout(
        title=f"Top {top_n} Produtos por Faturamento de Vendas",
        xaxis_title="Valor Total Vendido (R$)",
        yaxis_title="Produto",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig.to_dict()

def create_least_selling_chart_data(df_fin: pd.DataFrame, df_estoque: pd.DataFrame, top_n: int = 10) -> Dict:
    """
    Cria dados para gráfico dos N Produtos com Menor Faturamento.
    
    Args:
        df_fin: DataFrame de finanças (não usado, mantido para compatibilidade)
        df_estoque: DataFrame de estoque
        top_n: Número de produtos a retornar
        
    Returns:
        Dicionário com estrutura Plotly
    """
    least_selling = financial_analysis.get_least_selling_items(df_fin, df_estoque, top_n=top_n)
    
    if least_selling.empty:
        return {"data": [], "layout": {}}
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=least_selling.values,
        y=least_selling.index,
        orientation='h',
        marker_color='#F39C12',
        name='Faturamento'
    ))
    
    fig.update_layout(
        title=f"{top_n} Produtos com Menor Faturamento",
        xaxis_title="Valor Total Vendido (R$)",
        yaxis_title="Produto",
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(range=[0, max(1, least_selling.max() * 1.1)])
    )
    
    return fig.to_dict()

def create_stock_rupture_chart_data(df_estoque: pd.DataFrame, top_n: int = 10) -> Dict:
    """
    Cria dados para gráfico de Maiores Rupturas de Estoque.
    
    Args:
        df_estoque: DataFrame de estoque
        top_n: Número de produtos a retornar
        
    Returns:
        Dicionário com estrutura Plotly
    """
    df_ruptura = inventory_analysis.get_low_stock_items(df_estoque, top_n=top_n)
    
    if df_ruptura.empty:
        return {"data": [], "layout": {}}
    
    df_sorted = df_ruptura.sort_values('gap', ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_sorted['gap'].values,
        y=df_sorted['Produto'].values,
        orientation='h',
        marker_color='#E74C3C',
        name='Gap de Estoque'
    ))
    
    fig.update_layout(
        title="Maiores Rupturas de Estoque (Gap)",
        xaxis_title="Gap",
        yaxis_title="Produto",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig.to_dict()

