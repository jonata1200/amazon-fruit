# modules/analysis/insights_analysis.py
import pandas as pd

def find_most_profitable_products(df_estoque: pd.DataFrame, top_n: int = 5):
    """Encontra os produtos mais lucrativos com base na margem de lucro."""
    cols = {'Nome_Produto', 'Preco_Custo', 'Preco_Venda'}
    if df_estoque is None or df_estoque.empty or not cols.issubset(df_estoque.columns):
        return "Dados insuficientes para calcular a lucratividade dos produtos."

    df = df_estoque.copy()
    df['Lucro_Unitario'] = pd.to_numeric(df['Preco_Venda'], errors='coerce') - pd.to_numeric(df['Preco_Custo'], errors='coerce')
    top_products = df.sort_values('Lucro_Unitario', ascending=False).head(top_n)
    
    insight = "🌟 **Produtos com Maior Margem de Lucro:**\n\n"
    for i, row in top_products.iterrows():
        insight += f"  {i+1}. **{row['Nome_Produto']}** (Lucro por unidade: R$ {row['Lucro_Unitario']:.2f})\n"
    return insight

def find_top_customers_by_spend(df_publico: pd.DataFrame, top_n: int = 5):
    """Encontra os clientes que mais gastam em média."""
    cols = {'Nome', 'Gasto_Medio'}
    if df_publico is None or df_publico.empty or not cols.issubset(df_publico.columns):
        return "Dados insuficientes para identificar os principais clientes."
        
    df = df_publico.copy()
    top_customers = df.sort_values('Gasto_Medio', ascending=False).head(top_n)
    
    insight = "👥 **Clientes com Maior Gasto Médio:**\n\n"
    for i, row in top_customers.iterrows():
        insight += f"  {i+1}. **{row['Nome']}** (Gasto médio: R$ {row['Gasto_Medio']:.2f})\n"
    return insight

def analyze_monthly_financial_trend(df_financas: pd.DataFrame):
    """Analisa a tendência financeira mensal (lucro ao longo do tempo)."""
    cols = {'Data', 'Valor', 'Tipo'}
    if df_financas is None or df_financas.empty or not cols.issubset(df_financas.columns):
        return "Dados financeiros insuficientes para analisar a tendência mensal."
        
    df = df_financas.copy()
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    df.dropna(subset=['Data'], inplace=True)
    
    df['Mes'] = df['Data'].dt.to_period('M')
    df['Valor_Sinalizado'] = df.apply(
        lambda row: row['Valor'] if 'entrada' in str(row['Tipo']).lower() else -row['Valor'], axis=1
    )
    
    monthly_profit = df.groupby('Mes')['Valor_Sinalizado'].sum().sort_index()
    
    if len(monthly_profit) < 2:
        return "📈 **Tendência Financeira:**\n\nÉ necessário ter dados de pelo menos dois meses para analisar uma tendência."
        
    last_month_profit = monthly_profit.iloc[-1]
    second_last_month_profit = monthly_profit.iloc[-2]
    
    insight = f"📈 **Tendência Financeira (Lucro Mensal):**\n\n"
    insight += f"  - Lucro do último mês ({monthly_profit.index[-1]}): R$ {last_month_profit:,.2f}\n"
    insight += f"  - Lucro do mês anterior ({monthly_profit.index[-2]}): R$ {second_last_month_profit:,.2f}\n\n"
    
    if last_month_profit > second_last_month_profit:
        insight += "  **Conclusão:** O lucro aumentou em relação ao mês anterior. Tendência positiva!"
    else:
        insight += "  **Conclusão:** O lucro diminuiu em relação ao mês anterior. Ponto de atenção."
        
    return insight