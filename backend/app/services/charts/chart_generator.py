# backend/app/services/charts/chart_generator.py

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Optional

# Importar funções de análise
from ..analysis import financial_analysis, inventory_analysis, suppliers_analysis, public_analysis, hr_analysis

# ======================================================================
# --- GRÁFICOS DO DASHBOARD GERAL ---
# ======================================================================

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

# ======================================================================
# --- GRÁFICOS DO DASHBOARD DE FINANÇAS ---
# ======================================================================

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

# ======================================================================
# --- GRÁFICOS DO DASHBOARD DE ESTOQUE ---
# ======================================================================

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

# ======================================================================
# --- GRÁFICOS DO DASHBOARD DE FORNECEDORES ---
# ======================================================================

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

# ======================================================================
# --- GRÁFICOS DO DASHBOARD DE PÚBLICO-ALVO ---
# ======================================================================

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

# ======================================================================
# --- GRÁFICOS DO DASHBOARD DE RECURSOS HUMANOS ---
# ======================================================================

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

