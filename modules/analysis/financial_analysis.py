# modules/analysis/financial_analysis.py
import pandas as pd

# (O início do arquivo com a função _get_change e calculate_financial_summary permanece o mesmo)
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
    """Retorna a distribuição de despesas por categoria."""
    if df is None or df.empty or not {'Categoria', 'Tipo', 'Valor'}.issubset(df.columns):
        return pd.Series(dtype='float64')
    expenses_df = df[df['Tipo'].astype(str).str.lower() == 'despesa']
    return expenses_df.groupby('Categoria')['Valor'].sum().sort_values(ascending=False)

# --- NOVA FUNÇÃO ADICIONADA AQUI ---
def get_revenue_distribution(df: pd.DataFrame, top_n: int = 5) -> pd.Series:
    """Retorna a distribuição de receitas por categoria."""
    if df is None or df.empty or not {'Categoria', 'Tipo', 'Valor'}.issubset(df.columns):
        return pd.Series(dtype='float64')
    
    # A lógica é a mesma da função de despesas, mas filtrando por 'receita'
    revenue_df = df[df['Tipo'].astype(str).str.lower() == 'receita']
    return revenue_df.groupby('Categoria')['Valor'].sum().sort_values(ascending=False).head(top_n)