# modules/dashboards/chart_generator.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from matplotlib.figure import Figure
from ..analysis.financial_analysis import get_top_selling_items, get_least_selling_items, get_expense_distribution, get_revenue_distribution
from ..analysis.inventory_analysis import get_low_stock_items
from ..analysis.suppliers_analysis import get_top_bottom_suppliers, get_suppliers_by_state, create_supplier_product_matrix
from ..analysis.public_analysis import get_clients_by_location, get_clients_by_gender, get_clients_by_channel
from ..analysis.hr_analysis import get_headcount_by_department, get_cost_by_department, get_headcount_by_role, get_hiring_over_time


# ======================================================================
# --- GRÁFICOS DO DASHBOARD GERAL ---
# ======================================================================

def create_general_evolution_chart(df_fin: pd.DataFrame) -> Figure:
    """
    Cria o gráfico de Evolução Mensal com Faturamento e Lucro como
    barras agrupadas, com as barras de lucro negativo coloridas em vermelho.
    """
    fig, ax = plt.subplots(figsize=(10, 6), tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    if not df_fin.empty and 'Data' in df_fin.columns:
        # 1. Preparação dos dados mensais (sem alterações)
        df_fin['MesAno'] = pd.to_datetime(df_fin['Data'], errors='coerce').dt.to_period('M').astype(str)
        monthly = df_fin.groupby(['MesAno', 'Tipo'])['Valor'].sum().unstack(fill_value=0)
        
        if 'Receita' not in monthly.columns: monthly['Receita'] = 0
        if 'Despesa' not in monthly.columns: monthly['Despesa'] = 0
            
        monthly['Lucro'] = monthly['Receita'] - monthly['Despesa']

        # --- NOVA LÓGICA DE PLOTAGEM COM CORES DINÂMICAS ---

        # 2. Cria a lista de cores para as barras de lucro
        #    Vermelho para prejuízo, Verde Escuro para lucro.
        profit_colors = ['#C21807' if valor < 0 else '#006400' for valor in monthly['Lucro']]

        # 3. Configurações para as barras agrupadas
        n_months = len(monthly.index)
        ind = np.arange(n_months)  # posições dos grupos no eixo x
        width = 0.4  # largura das barras

        # 4. Plota as barras de Faturamento (sempre roxas)
        #    Elas são desenhadas um pouco para a esquerda do centro do mês
        rects1 = ax.bar(ind - width/2, monthly['Receita'], width, label='Faturamento (Receita)', color='#6A0DAD')

        # 5. Plota as barras de Lucro usando a lista de cores dinâmica
        #    Elas são desenhadas um pouco para a direita do centro do mês
        rects2 = ax.bar(ind + width/2, monthly['Lucro'], width, label='Lucro Líquido', color=profit_colors)
        
        # --- FIM DA NOVA LÓGICA ---

        # 6. Configuração dos eixos e legendas
        ax.set_title("Evolução Mensal: Faturamento vs. Lucro", fontsize=16)
        ax.set_ylabel("Valor (R$)")
        ax.set_xticks(ind)
        ax.set_xticklabels(monthly.index, rotation=45, ha="right", rotation_mode="anchor")
        
        ax.get_yaxis().set_major_formatter(
            plt.FuncFormatter(lambda x, p: format(int(x), ','))
        )
        ax.legend()
        
        # Adiciona uma linha de referência no zero para clareza visual
        ax.axhline(0, color='grey', linewidth=0.8)

    return fig

# ======================================================================
# --- GRÁFICOS DO DASHBOARD DE FINANÇAS ---
# ======================================================================

def create_finance_evolution_chart(df_fin: pd.DataFrame) -> Figure:
    """Cria o gráfico de Evolução Financeira Mensal (Receita x Despesa x Lucro)."""
    fig, ax1 = plt.subplots(tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF'); ax1.set_facecolor('#FFFFFF')
    
    if not df_fin.empty and 'Data' in df_fin.columns:
        df_fin['MesAno'] = pd.to_datetime(df_fin['Data'], errors='coerce').dt.to_period('M').astype(str)
        monthly = df_fin.groupby(['MesAno', 'Tipo'])['Valor'].sum().unstack(fill_value=0)
        monthly['Lucro'] = monthly.get('Receita', 0) - monthly.get('Despesa', 0)
        
        monthly[['Receita', 'Despesa']].plot(kind='bar', ax=ax1, color=['#2E8B57', '#C21807'])
        ax1_lucro = ax1.twinx()
        monthly['Lucro'].plot(kind='line', ax=ax1_lucro, color='#FF8C00', marker='o')
        ax1.set_title("Evolução Financeira Mensal")
        
    return fig

def create_top_expenses_chart(df_fin: pd.DataFrame) -> Figure:
    """Cria o gráfico de Top 5 Despesas por Categoria."""
    fig, ax = plt.subplots(tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF'); ax.set_facecolor('#FFFFFF')
    ser_exp = get_expense_distribution(df_fin).head(5)
    if not ser_exp.empty: ser_exp.sort_values().plot(kind='barh', ax=ax, color='#C21807')
    ax.set_title("Top 5 Despesas por Categoria")
    return fig

def create_top_revenues_chart(df_fin: pd.DataFrame) -> Figure:
    """Cria o gráfico de Top 5 Receitas por Categoria."""
    fig, ax = plt.subplots(tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF'); ax.set_facecolor('#FFFFFF')
    ser_rev = get_revenue_distribution(df_fin, top_n=5)
    if not ser_rev.empty: ser_rev.sort_values().plot(kind='barh', ax=ax, color='#2E8B57')
    ax.set_title("Top 5 Receitas por Categoria")
    return fig

# ======================================================================
# --- GRÁFICOS DO DASHBOARD DE ESTOQUE ---
# ======================================================================

def create_top_selling_chart(df_fin: pd.DataFrame, df_estoque: pd.DataFrame) -> Figure:
    """Cria o gráfico de Top 10 Produtos por Faturamento."""
    fig, ax = plt.subplots(tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF'); ax.set_facecolor('#FFFFFF')
    ser_prod = get_top_selling_items(df_fin, df_estoque, top_n=10)
    if not ser_prod.empty: ser_prod.sort_values().plot(kind='barh', ax=ax, color='#2ECC71')
    ax.set_title("Top 10 Produtos por Faturamento de Vendas"); ax.set_ylabel(""), ax.set_xlabel("Valor Total Vendido (R$)")
    return fig

def create_least_selling_chart(df_fin: pd.DataFrame, df_estoque: pd.DataFrame) -> Figure:
    """Cria o gráfico dos 10 Produtos com Menor Faturamento."""
    fig, ax = plt.subplots(tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF'); ax.set_facecolor('#FFFFFF')
    ser_least = get_least_selling_items(df_fin, df_estoque, top_n=10)
    
    if not ser_least.empty:
        ser_least.sort_values(ascending=False).plot(kind='barh', ax=ax, color='#F39C12')
        # --- MUDANÇA AQUI ---
        # Define o limite esquerdo do eixo X como 0.
        # Isso garante que as barras de valor zero tenham uma linha de base visível.
        # Adicionamos um pequeno espaço à direita para o faturamento máximo, caso não seja zero.
        ax.set_xlim(left=0, right=max(1, ser_least.max() * 1.1))
        # --- FIM DA MUDANÇA ---

    ax.set_title("10 Produtos com Menor Faturamento"); ax.set_ylabel(""), ax.set_xlabel("Valor Total Vendido (R$)")
    return fig
    
def create_stock_rupture_chart(df_estoque: pd.DataFrame) -> Figure:
    """Cria o gráfico de Maiores Rupturas de Estoque."""
    fig, ax = plt.subplots(tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF'); ax.set_facecolor('#FFFFFF')
    df_ruptura = get_low_stock_items(df_estoque, top_n=10)
    
    # --- MUDANÇA AQUI: Corrigido de x='Nome_Produto' para x='Produto' ---
    if not df_ruptura.empty: 
        df_ruptura.sort_values('gap', ascending=True).plot(kind='barh', x='Produto', y='gap', ax=ax, legend=False, color='#E74C3C')

    ax.set_title("Maiores Rupturas de Estoque (Gap)"); ax.set_ylabel("")
    return fig

# ======================================================================
# --- GRÁFICOS DO DASHBOARD DE FORNECEDORES ---
# ======================================================================

def create_supplier_ranking_chart(df_fornecedores: pd.DataFrame) -> Figure:
    """Cria os gráficos de Top e Bottom 5 Fornecedores."""
    fig, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(6, 8), tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF')
    suppliers = get_top_bottom_suppliers(df_fornecedores, n=5)
    if not suppliers['top'].empty:
        suppliers['top'].sort_values('Avaliacao', ascending=True).plot(kind='barh', x='Nome_Fornecedor', y='Avaliacao', ax=ax_top, color='#2ECC71', legend=False)
        ax_top.set_title("Top 5 Melhores Fornecedores"); ax_top.set_xlim(0, 5)
    if not suppliers['bottom'].empty:
        suppliers['bottom'].sort_values('Avaliacao', ascending=False).plot(kind='barh', x='Nome_Fornecedor', y='Avaliacao', ax=ax_bottom, color='#E74C3C', legend=False)
        ax_bottom.set_title("Top 5 Piores Fornecedores"); ax_bottom.set_xlim(0, 5)
    return fig

def create_supplier_geo_chart(df_fornecedores: pd.DataFrame) -> Figure:
    """Cria o gráfico de Distribuição de Fornecedores por Estado."""
    fig, ax = plt.subplots(tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF'); ax.set_facecolor('#FFFFFF')
    by_state = get_suppliers_by_state(df_fornecedores)
    if not by_state.empty: by_state.sort_values().plot(kind='barh', ax=ax, color='#3498DB')
    ax.set_title("Distribuição de Fornecedores por Estado")
    return fig

def create_supplier_heatmap(df_fornecedores: pd.DataFrame) -> Figure:
    """Cria a Matriz de Fornecedores por Produtos."""
    fig, ax = plt.subplots(figsize=(10, 8), tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF')
    matrix = create_supplier_product_matrix(df_fornecedores)
    if not matrix.empty:
        sns.heatmap(matrix, ax=ax, cmap="YlGn", linewidths=.5, linecolor='lightgray', cbar=False)
        ax.set_title("Matriz de Fornecedores por Produtos", fontsize=14)
    return fig
    
# ======================================================================
# --- GRÁFICOS DO DASHBOARD DE PÚBLICO-ALVO ---
# ======================================================================

def create_public_location_chart(df_publico: pd.DataFrame) -> Figure:
    """Cria o gráfico de Top 10 Clientes por Localização (Cidade)."""
    fig, ax = plt.subplots(tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF'); ax.set_facecolor('#FFFFFF')
    
    ser_loc = get_clients_by_location(df_publico, top_n=10)
    if not ser_loc.empty:
        ser_loc.sort_values().plot(kind='barh', ax=ax, color='#6A0DAD')
    
    ax.set_title("Top 10 Clientes por Localização")
    return fig

def create_public_gender_chart(df_publico: pd.DataFrame) -> Figure:
    """Cria o gráfico de pizza de Distribuição por Gênero."""
    fig, ax = plt.subplots(tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF'); ax.set_facecolor('#FFFFFF')
    
    ser_gen = get_clients_by_gender(df_publico)
    if not ser_gen.empty:
        color_map = {"Feminino": "#FF69B4", "Masculino": "#1E90FF"}
        pie_colors = [color_map.get(label, '#CCCCCC') for label in ser_gen.index]
        ax.pie(ser_gen.values, labels=ser_gen.index, autopct='%1.1f%%', startangle=90, colors=pie_colors)

    ax.set_title("Distribuição por Gênero")
    return fig

def create_public_channel_chart(df_publico: pd.DataFrame) -> Figure:
    """Cria o gráfico de Contagem de Clientes por Canal de Venda."""
    fig, ax = plt.subplots(tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF'); ax.set_facecolor('#FFFFFF')
    
    ser_canal = get_clients_by_channel(df_publico)
    if not ser_canal.empty:
        ser_canal.sort_values().plot(kind='barh', ax=ax, color='#FFA500')
    
    ax.set_title("Contagem de Clientes por Canal de Venda")
    return fig

# ======================================================================
# --- GRÁFICOS DO DASHBOARD DE RECURSOS HUMANOS ---
# ======================================================================

def create_hr_headcount_chart(df_rh: pd.DataFrame) -> Figure:
    """Cria o gráfico de Nº de Funcionários por Departamento."""
    fig, ax = plt.subplots(tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF'); ax.set_facecolor('#FFFFFF')
    
    headcount = get_headcount_by_department(df_rh)
    if not headcount.empty:
        headcount.sort_values().plot(kind='barh', ax=ax, color='#6A0DAD')
        
    ax.set_title("Nº de Funcionários por Depto.")
    return fig

def create_hr_cost_chart(df_rh: pd.DataFrame) -> Figure:
    """Cria o gráfico de Custo Mensal por Departamento."""
    fig, ax = plt.subplots(tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF'); ax.set_facecolor('#FFFFFF')
    
    cost = get_cost_by_department(df_rh)
    if not cost.empty:
        cost.plot(kind='barh', ax=ax, color='#3498DB')
        
    ax.set_title("Custo Mensal por Depto.")
    return fig

def create_hr_role_chart(df_rh: pd.DataFrame) -> Figure:
    """Cria o gráfico de Top 10 Cargos na Empresa."""
    fig, ax = plt.subplots(tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF'); ax.set_facecolor('#FFFFFF')
    
    roles = get_headcount_by_role(df_rh)
    if not roles.empty:
        roles.sort_values().plot(kind='barh', ax=ax, color='#2ECC71')
        
    ax.set_title("Top 10 Cargos na Empresa")
    return fig

def create_hr_hiring_chart(df_rh: pd.DataFrame) -> Figure:
    """Cria o gráfico de Histórico de Contratações ao Longo do Tempo."""
    fig, ax = plt.subplots(tight_layout=True)
    fig.patch.set_facecolor('#FFFFFF'); ax.set_facecolor('#FFFFFF')
    
    hiring = get_hiring_over_time(df_rh)
    if not hiring.empty:
        hiring.plot(kind='line', ax=ax, marker='o', color='#E67E22')
        
    ax.set_title("Contratações ao Longo do Tempo")
    ax.tick_params(axis='x', rotation=45, labelsize=8)
    return fig