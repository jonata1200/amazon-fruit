# backend/app/services/charts/suppliers_charts.py

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict

# Importar funções de análise
from ..analysis import suppliers_analysis

def create_supplier_ranking_chart_data(df_fornecedores: pd.DataFrame, n: int = 5) -> Dict:
    """
    Cria dados para gráficos de Top e Bottom N Fornecedores.
    
    Args:
        df_fornecedores: DataFrame de fornecedores
        n: Número de fornecedores em cada categoria
        
    Returns:
        Dicionário com estrutura Plotly para dois gráficos
    """
    suppliers = suppliers_analysis.get_top_bottom_suppliers(df_fornecedores, n=n)
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=("Top 5 Melhores Fornecedores", "Top 5 Piores Fornecedores"),
        vertical_spacing=0.15
    )
    
    if not suppliers['top'].empty:
        top_sorted = suppliers['top'].sort_values('Avaliacao', ascending=True)
        fig.add_trace(go.Bar(
            x=top_sorted['Avaliacao'].values,
            y=top_sorted['Nome_Fornecedor'].values,
            orientation='h',
            marker_color='#2ECC71',
            name='Top'
        ), row=1, col=1)
        fig.update_xaxes(range=[0, 5], row=1, col=1)
    
    if not suppliers['bottom'].empty:
        bottom_sorted = suppliers['bottom'].sort_values('Avaliacao', ascending=False)
        fig.add_trace(go.Bar(
            x=bottom_sorted['Avaliacao'].values,
            y=bottom_sorted['Nome_Fornecedor'].values,
            orientation='h',
            marker_color='#E74C3C',
            name='Bottom'
        ), row=2, col=1)
        fig.update_xaxes(range=[0, 5], row=2, col=1)
    
    fig.update_layout(
        height=600,
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    
    return fig.to_dict()

def create_supplier_geo_chart_data(df_fornecedores: pd.DataFrame) -> Dict:
    """
    Cria dados para gráfico de Distribuição de Fornecedores por Estado.
    
    Args:
        df_fornecedores: DataFrame de fornecedores
        
    Returns:
        Dicionário com estrutura Plotly
    """
    by_state = suppliers_analysis.get_suppliers_by_state(df_fornecedores)
    
    if by_state.empty:
        return {"data": [], "layout": {}}
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=by_state.values,
        y=by_state.index,
        orientation='h',
        marker_color='#3498DB',
        name='Fornecedores'
    ))
    
    fig.update_layout(
        title="Distribuição de Fornecedores por Estado",
        xaxis_title="Número de Fornecedores",
        yaxis_title="Estado",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig.to_dict()

