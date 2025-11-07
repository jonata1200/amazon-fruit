# modules/analysis/financial_analysis.py
import pandas as pd

def _get_change(current, previous):
    if previous is None or pd.isna(previous) or previous == 0: return None
    return (current - previous) / previous

def calculate_financial_summary(df_current: pd.DataFrame, df_previous: pd.DataFrame = None) -> dict:
    def _calculate(df):
        if df is None or df.empty: return {'receita': 0.0, 'despesa': 0.0, 'lucro': 0.0}
        t = df['Tipo'].astype(str).str.lower()
        v = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        receita = float(v[t.str.contains('receita', case=False)].sum())
        despesa = float(v[t.str.contains('despesa', case=False)].sum())
        return {'receita': receita, 'despesa': despesa, 'lucro': receita - despesa}
    summary_current = _calculate(df_current)
    summary_previous = _calculate(df_previous)
    summary_current['receita_change'] = _get_change(summary_current['receita'], summary_previous['receita'])
    summary_current['despesa_change'] = _get_change(summary_current['despesa'], summary_previous['despesa'])
    summary_current['lucro_change'] = _get_change(summary_current['lucro'], summary_previous['lucro'])
    return summary_current

def get_expense_distribution(df: pd.DataFrame) -> pd.Series:
    if df is None or df.empty or not {'Categoria', 'Tipo', 'Valor'}.issubset(df.columns):
        return pd.Series(dtype='float64')
    expenses_df = df[df['Tipo'].astype(str).str.lower() == 'despesa']
    return expenses_df.groupby('Categoria')['Valor'].sum().sort_values(ascending=False)

def get_revenue_distribution(df: pd.DataFrame, top_n: int = 5) -> pd.Series:
    if df is None or df.empty or not {'Categoria', 'Tipo', 'Valor'}.issubset(df.columns):
        return pd.Series(dtype='float64')
    revenue_df = df[df['Tipo'].astype(str).str.lower() == 'receita']
    return revenue_df.groupby('Categoria')['Valor'].sum().sort_values(ascending=False).head(top_n)

def get_top_selling_items(df_financas: pd.DataFrame, df_estoque: pd.DataFrame, top_n: int = 10) -> pd.Series:
    """
    Identifica os produtos mais vendidos a partir dos DADOS DE ESTOQUE.
    """
    if df_estoque is None or df_estoque.empty:
        return pd.Series(dtype='float64')

    # --- MUDANÇA PRINCIPAL AQUI ---
    # O nome da coluna foi corrigido de 'Nome_Produto' para 'Produto'.
    required_cols = {'Produto', 'Quantidade_Vendida', 'Preco_Venda'}
    if not required_cols.issubset(df_estoque.columns):
        # Adiciona um print para ajudar a depurar caso o erro ocorra novamente
        print(f"Erro em 'get_top_selling_items': Colunas necessárias não encontradas. Colunas disponíveis: {list(df_estoque.columns)}")
        return pd.Series(dtype='float64')

    sales_df = df_estoque.copy()
    sales_df['Quantidade_Vendida'] = pd.to_numeric(sales_df['Quantidade_Vendida'], errors='coerce').fillna(0)
    sales_df['Preco_Venda'] = pd.to_numeric(sales_df['Preco_Venda'], errors='coerce').fillna(0)
    sales_df['Faturamento'] = sales_df['Quantidade_Vendida'] * sales_df['Preco_Venda']

    # --- MUDANÇA AQUI TAMBÉM ---
    top_selling = sales_df.groupby('Produto')['Faturamento'].sum()
    
    return top_selling.sort_values(ascending=False).head(top_n)

def get_least_selling_items(df_financas: pd.DataFrame, df_estoque: pd.DataFrame, top_n: int = 10) -> pd.Series:
    """
    Identifica os produtos menos vendidos, incluindo aqueles que nunca foram vendidos.
    """
    if df_estoque is None or df_estoque.empty:
        return pd.Series(dtype='float64')

    # --- MUDANÇA PRINCIPAL AQUI ---
    # O nome da coluna foi corrigido de 'Nome_Produto' para 'Produto'.
    if 'Produto' not in df_estoque.columns:
        print(f"Erro em 'get_least_selling_items': Coluna 'Produto' não encontrada. Colunas disponíveis: {list(df_estoque.columns)}")
        return pd.Series(dtype='float64')

    all_products = df_estoque[['Produto']].drop_duplicates().set_index('Produto')

    sales_df = df_estoque.copy()
    sales_df['Quantidade_Vendida'] = pd.to_numeric(sales_df['Quantidade_Vendida'], errors='coerce').fillna(0)
    sales_df['Preco_Venda'] = pd.to_numeric(sales_df['Preco_Venda'], errors='coerce').fillna(0)
    sales_df['Faturamento'] = sales_df['Quantidade_Vendida'] * sales_df['Preco_Venda']

    # --- MUDANÇA AQUI TAMBÉM ---
    sales_summary = sales_df.groupby('Produto')['Faturamento'].sum()

    combined = all_products.join(sales_summary)
    least_selling = combined.fillna(0).sort_values('Faturamento', ascending=True).head(top_n)

    return least_selling['Faturamento']