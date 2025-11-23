# backend/app/services/charts/general_charts.py

import pandas as pd
import plotly.graph_objects as go
from typing import Dict

def create_general_evolution_chart_data(df_fin: pd.DataFrame) -> Dict:
    """
    Cria dados para gráfico de Evolução Mensal com Faturamento e Lucro.
    Retorna estrutura Plotly JSON.
    
    Args:
        df_fin: DataFrame com dados financeiros
        
    Returns:
        Dicionário com estrutura Plotly
    """
    if df_fin.empty or 'Data' not in df_fin.columns:
        return {"data": [], "layout": {}}
    
    # Preparação dos dados mensais
    df_fin_copy = df_fin.copy()
    df_fin_copy['MesAno'] = pd.to_datetime(df_fin_copy['Data'], errors='coerce').dt.to_period('M').astype(str)
    monthly = df_fin_copy.groupby(['MesAno', 'Tipo'])['Valor'].sum().unstack(fill_value=0)
    
    if 'Receita' not in monthly.columns:
        monthly['Receita'] = 0
    if 'Despesa' not in monthly.columns:
        monthly['Despesa'] = 0
        
    monthly['Lucro'] = monthly['Receita'] - monthly['Despesa']
    
    # Criar figura Plotly
    fig = go.Figure()
    
    # Barra de Receita (roxo)
    fig.add_trace(go.Bar(
        x=monthly.index,
        y=monthly['Receita'],
        name='Faturamento (Receita)',
        marker_color='#6A0DAD',
        offsetgroup=1
    ))
    
    # Barras de Lucro com cores dinâmicas
    profit_colors = ['#C21807' if valor < 0 else '#006400' for valor in monthly['Lucro']]
    fig.add_trace(go.Bar(
        x=monthly.index,
        y=monthly['Lucro'],
        name='Lucro Líquido',
        marker_color=profit_colors,
        offsetgroup=2
    ))
    
    # Layout
    fig.update_layout(
        title="Evolução Mensal: Faturamento vs. Lucro",
        xaxis_title="Mês",
        yaxis_title="Valor (R$)",
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified'
    )
    
    return fig.to_dict()

