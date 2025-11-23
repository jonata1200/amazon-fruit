# backend/app/services/charts/finance_charts.py

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict

# Importar funções de análise
from ..analysis import financial_analysis

def create_finance_evolution_chart_data(df_fin: pd.DataFrame) -> Dict:
    """
    Cria dados para gráfico de Evolução Financeira Mensal (Receita x Despesa x Lucro).
    
    Args:
        df_fin: DataFrame com dados financeiros
        
    Returns:
        Dicionário com estrutura Plotly
    """
    if df_fin.empty or 'Data' not in df_fin.columns:
        return {"data": [], "layout": {}}
    
    df_fin_copy = df_fin.copy()
    df_fin_copy['MesAno'] = pd.to_datetime(df_fin_copy['Data'], errors='coerce').dt.to_period('M').astype(str)
    monthly = df_fin_copy.groupby(['MesAno', 'Tipo'])['Valor'].sum().unstack(fill_value=0)
    monthly['Lucro'] = monthly.get('Receita', 0) - monthly.get('Despesa', 0)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Barras de Receita e Despesa
    fig.add_trace(go.Bar(x=monthly.index, y=monthly['Receita'], name='Receita', marker_color='#2E8B57'), secondary_y=False)
    fig.add_trace(go.Bar(x=monthly.index, y=monthly['Despesa'], name='Despesa', marker_color='#C21807'), secondary_y=False)
    
    # Linha de Lucro
    fig.add_trace(go.Scatter(x=monthly.index, y=monthly['Lucro'], name='Lucro', mode='lines+markers', marker_color='#FF8C00'), secondary_y=True)
    
    fig.update_layout(
        title="Evolução Financeira Mensal",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    fig.update_xaxes(title_text="Mês")
    fig.update_yaxes(title_text="Receita/Despesa (R$)", secondary_y=False)
    fig.update_yaxes(title_text="Lucro (R$)", secondary_y=True)
    
    return fig.to_dict()

def create_top_expenses_chart_data(df_fin: pd.DataFrame, top_n: int = 5) -> Dict:
    """
    Cria dados para gráfico de Top N Despesas por Categoria.
    
    Args:
        df_fin: DataFrame com dados financeiros
        top_n: Número de categorias a retornar
        
    Returns:
        Dicionário com estrutura Plotly
    """
    expenses = financial_analysis.get_expense_distribution(df_fin).head(top_n)
    
    if expenses.empty:
        return {"data": [], "layout": {}}
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=expenses.values,
        y=expenses.index,
        orientation='h',
        marker_color='#C21807',
        name='Despesas'
    ))
    
    fig.update_layout(
        title=f"Top {top_n} Despesas por Categoria",
        xaxis_title="Valor (R$)",
        yaxis_title="Categoria",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig.to_dict()

def create_top_revenues_chart_data(df_fin: pd.DataFrame, top_n: int = 5) -> Dict:
    """
    Cria dados para gráfico de Top N Receitas por Categoria.
    
    Args:
        df_fin: DataFrame com dados financeiros
        top_n: Número de categorias a retornar
        
    Returns:
        Dicionário com estrutura Plotly
    """
    revenues = financial_analysis.get_revenue_distribution(df_fin, top_n=top_n)
    
    if revenues.empty:
        return {"data": [], "layout": {}}
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=revenues.values,
        y=revenues.index,
        orientation='h',
        marker_color='#2E8B57',
        name='Receitas'
    ))
    
    fig.update_layout(
        title=f"Top {top_n} Receitas por Categoria",
        xaxis_title="Valor (R$)",
        yaxis_title="Categoria",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig.to_dict()

