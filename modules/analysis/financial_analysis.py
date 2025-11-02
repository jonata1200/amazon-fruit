# modules/analysis/financial_analysis.py
import pandas as pd

def calculate_financial_summary(df: pd.DataFrame) -> dict:
    """Calcula o resumo financeiro (receita, despesa, lucro) a partir de um DataFrame."""
    if df is None or df.empty or not {'Valor', 'Tipo'}.issubset(df.columns):
        return {'receita': 0.0, 'despesa': 0.0, 'lucro': 0.0}

    t = df['Tipo'].astype(str).str.lower()
    v = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
    
    receita = float(v[t.str.contains('entrada', case=False)].sum())
    despesa = float(v[t.str.contains('saída', case=False)].sum())
    lucro = receita - despesa

    return {'receita': receita, 'despesa': despesa, 'lucro': lucro}

def get_expense_distribution(df: pd.DataFrame) -> pd.Series:
    """Retorna a distribuição de despesas por categoria."""
    if df is None or df.empty or not {'Categoria', 'Tipo', 'Valor'}.issubset(df.columns):
        return pd.Series(dtype='float64')
    
    expenses_df = df[df['Tipo'].astype(str).str.lower().str.contains('saída', case=False)]
    return expenses_df.groupby('Categoria')['Valor'].sum().sort_values(ascending=False)