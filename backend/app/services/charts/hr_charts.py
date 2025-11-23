# backend/app/services/charts/hr_charts.py

import pandas as pd
import plotly.graph_objects as go
from typing import Dict

# Importar funções de análise
from ..analysis import hr_analysis

def create_hr_headcount_chart_data(df_rh: pd.DataFrame) -> Dict:
    """
    Cria dados para gráfico de Nº de Funcionários por Departamento.
    
    Args:
        df_rh: DataFrame de RH
        
    Returns:
        Dicionário com estrutura Plotly
    """
    headcount = hr_analysis.get_headcount_by_department(df_rh)
    
    if headcount.empty:
        return {"data": [], "layout": {}}
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=headcount.values,
        y=headcount.index,
        orientation='h',
        marker_color='#6A0DAD',
        name='Funcionários'
    ))
    
    fig.update_layout(
        title="Nº de Funcionários por Depto.",
        xaxis_title="Número de Funcionários",
        yaxis_title="Departamento",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig.to_dict()

def create_hr_cost_chart_data(df_rh: pd.DataFrame) -> Dict:
    """
    Cria dados para gráfico de Custo Mensal por Departamento.
    
    Args:
        df_rh: DataFrame de RH
        
    Returns:
        Dicionário com estrutura Plotly
    """
    costs = hr_analysis.get_cost_by_department(df_rh)
    
    if costs.empty:
        return {"data": [], "layout": {}}
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=costs.values,
        y=costs.index,
        orientation='h',
        marker_color='#3498DB',
        name='Custo'
    ))
    
    fig.update_layout(
        title="Custo Mensal por Depto.",
        xaxis_title="Custo Mensal (R$)",
        yaxis_title="Departamento",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig.to_dict()

def create_hr_role_chart_data(df_rh: pd.DataFrame) -> Dict:
    """
    Cria dados para gráfico de Top 10 Cargos na Empresa.
    
    Args:
        df_rh: DataFrame de RH
        
    Returns:
        Dicionário com estrutura Plotly
    """
    roles = hr_analysis.get_headcount_by_role(df_rh)
    
    if roles.empty:
        return {"data": [], "layout": {}}
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=roles.values,
        y=roles.index,
        orientation='h',
        marker_color='#2ECC71',
        name='Funcionários'
    ))
    
    fig.update_layout(
        title="Top 10 Cargos na Empresa",
        xaxis_title="Número de Funcionários",
        yaxis_title="Cargo",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig.to_dict()

def create_hr_hiring_chart_data(df_rh: pd.DataFrame) -> Dict:
    """
    Cria dados para gráfico de Histórico de Contratações ao Longo do Tempo.
    
    Args:
        df_rh: DataFrame de RH
        
    Returns:
        Dicionário com estrutura Plotly
    """
    hiring = hr_analysis.get_hiring_over_time(df_rh)
    
    if hiring.empty:
        return {"data": [], "layout": {}}
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hiring.index,
        y=hiring.values,
        mode='lines+markers',
        marker_color='#E67E22',
        name='Contratações'
    ))
    
    fig.update_layout(
        title="Contratações ao Longo do Tempo",
        xaxis_title="Período",
        yaxis_title="Número de Contratações",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig.to_dict()

