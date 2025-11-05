# modules/analysis/financial_analysis.py

from modules.utils.data_handler import DataRepository
import pandas as pd

repo = DataRepository()

def df_base():
    return repo.load_financas()

def kpis_mensais():
    df = repo.load_financas()
    df["AnoMes"] = df["Data"].dt.to_period("M").astype(str)
    tot = df.groupby(["AnoMes","Tipo"], as_index=False)["Valor"].sum()
    pivot = tot.pivot(index="AnoMes", columns="Tipo", values="Valor").fillna(0)
    pivot["Saldo"] = pivot.get("Receita",0) - pivot.get("Despesa",0)
    return pivot.reset_index()

def top5_categorias(periodo:str|None=None):
    df = repo.load_financas()
    if periodo:
        df = df[df["Data"].dt.to_period("M").astype(str).eq(periodo)]
    return (df.groupby(["Tipo","Categoria"], as_index=False)["Valor"]
              .sum().sort_values("Valor", ascending=False).head(5))

def get_expense_distribution(df: pd.DataFrame) -> pd.Series:
    """Retorna a distribuição de despesas por categoria."""
    if df is None or df.empty or not {'Categoria', 'Tipo', 'Valor'}.issubset(df.columns):
        return pd.Series(dtype='float64')
    
    expenses_df = df[df['Tipo'].astype(str).str.lower() == 'despesa']
    return expenses_df.groupby('Categoria')['Valor'].sum().sort_values(ascending=False)

def _get_change(current, previous):
    """Calcula a variação percentual de forma segura, evitando divisão por zero."""
    if previous is None or pd.isna(previous) or previous == 0:
        return None # Não é possível calcular a variação
    return (current - previous) / previous

def calculate_financial_summary(df_current: pd.DataFrame, df_previous: pd.DataFrame = None) -> dict:
    """
    Calcula o resumo financeiro para o período atual e a variação em relação ao anterior.
    """
    # Função interna para evitar repetição de código
    def _calculate(df):
        if df is None or df.empty:
            return {'receita': 0.0, 'despesa': 0.0, 'lucro': 0.0}
        t = df['Tipo'].astype(str).str.lower()
        v = pd.to_numeric(df['Valor'], errors='coerce').fillna(0.0)
        receita = float(v[t.str.contains('receita', case=False)].sum())
        despesa = float(v[t.str.contains('despesa', case=False)].sum())
        return {'receita': receita, 'despesa': despesa, 'lucro': receita - despesa}

    # Calcula para os dois períodos
    summary_current = _calculate(df_current)
    summary_previous = _calculate(df_previous)

    # Adiciona a variação ao resultado
    summary_current['receita_change'] = _get_change(summary_current['receita'], summary_previous['receita'])
    summary_current['despesa_change'] = _get_change(summary_current['despesa'], summary_previous['despesa'])
    summary_current['lucro_change'] = _get_change(summary_current['lucro'], summary_previous['lucro'])

    return summary_current