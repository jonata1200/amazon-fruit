# backend/app/services/charts/public_charts.py

import pandas as pd
import plotly.graph_objects as go
from typing import Dict

# Importar funções de análise
from ..analysis import public_analysis

def create_public_location_chart_data(df_publico: pd.DataFrame, top_n: int = 10) -> Dict:
    """
    Cria dados para gráfico de Top N Clientes por Localização.
    
    Args:
        df_publico: DataFrame de público-alvo
        top_n: Número de localizações a retornar
        
    Returns:
        Dicionário com estrutura Plotly
    """
    by_location = public_analysis.get_clients_by_location(df_publico, top_n=top_n)
    
    if by_location.empty:
        return {"data": [], "layout": {}}
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=by_location.values,
        y=by_location.index,
        orientation='h',
        marker_color='#6A0DAD',
        name='Clientes'
    ))
    
    fig.update_layout(
        title=f"Top {top_n} Clientes por Localização",
        xaxis_title="Número de Clientes",
        yaxis_title="Cidade",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig.to_dict()

def create_public_gender_chart_data(df_publico: pd.DataFrame) -> Dict:
    """
    Cria dados para gráfico de pizza de Distribuição por Gênero.
    
    Args:
        df_publico: DataFrame de público-alvo
        
    Returns:
        Dicionário com estrutura Plotly
    """
    by_gender = public_analysis.get_clients_by_gender(df_publico)
    
    if by_gender.empty:
        return {"data": [], "layout": {}}
    
    color_map = {"Feminino": "#FF69B4", "Masculino": "#1E90FF"}
    colors = [color_map.get(label, '#CCCCCC') for label in by_gender.index]
    
    fig = go.Figure(data=[go.Pie(
        labels=by_gender.index,
        values=by_gender.values,
        marker_colors=colors
    )])
    
    fig.update_layout(
        title="Distribuição por Gênero",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig.to_dict()

def create_public_channel_chart_data(df_publico: pd.DataFrame) -> Dict:
    """
    Cria dados para gráfico de Contagem de Clientes por Canal de Venda.
    
    Args:
        df_publico: DataFrame de público-alvo
        
    Returns:
        Dicionário com estrutura Plotly
    """
    by_channel = public_analysis.get_clients_by_channel(df_publico)
    
    if by_channel.empty:
        return {"data": [], "layout": {}}
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=by_channel.values,
        y=by_channel.index,
        orientation='h',
        marker_color='#FFA500',
        name='Clientes'
    ))
    
    fig.update_layout(
        title="Contagem de Clientes por Canal de Venda",
        xaxis_title="Número de Clientes",
        yaxis_title="Canal",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig.to_dict()

