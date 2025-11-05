# modules/analysis/inventory_analysis.py

from modules.utils.data_handler import DataRepository
import pandas as pd

repo = DataRepository()

def snapshot():
    return repo.load_estoque_snapshot()

def estoque_por_mes():
    df = repo.load_estoque_snapshot()
    df["AnoMes"] = df["Data_Snapshot"].dt.to_period("M").astype(str)
    return (df.groupby(["AnoMes"], as_index=False)["Quantidade_Estoque"]
              .sum().rename(columns={"Quantidade_Estoque":"Qtd_Total"}))

def rupturas():
    df = repo.load_estoque_snapshot()
    ult = df.sort_values("Data_Snapshot").groupby("ID_Produto").tail(1)
    return ult[ult["Quantidade_Estoque"] < ult["Nivel_Minimo_Estoque"]]

def _get_change(current, previous):
    if previous is None or pd.isna(previous) or previous == 0:
        return None
    return (current - previous) / previous

def analyze_inventory_kpis(df_current: pd.DataFrame, df_previous: pd.DataFrame = None) -> dict:
    """Analisa e retorna os KPIs de estoque para o período atual e a variação."""
    
    def _calculate(df: pd.DataFrame):
        if df is None or df.empty:
            return {'unique_products': 0, 'total_value': 0.0, 'low_stock_count': 0}
        
        unique_products = df['ID_Produto'].nunique() if 'ID_Produto' in df.columns else len(df)
        
        total_value = 0.0
        if {'Quantidade_Estoque', 'Preco_Custo'}.issubset(df.columns):
            q = pd.to_numeric(df['Quantidade_Estoque'], errors='coerce').fillna(0)
            c = pd.to_numeric(df['Preco_Custo'], errors='coerce').fillna(0.0)
            total_value = float((q * c).sum())
            
        low_stock_count = 0
        if {'Quantidade_Estoque', 'Nivel_Minimo_Estoque'}.issubset(df.columns):
            q2 = pd.to_numeric(df['Quantidade_Estoque'], errors='coerce')
            n2 = pd.to_numeric(df['Nivel_Minimo_Estoque'], errors='coerce')
            low_stock_count = int((q2 <= n2).sum())
            
        return {
            'unique_products': unique_products,
            'total_value': total_value,
            'low_stock_count': low_stock_count
        }

    summary_current = _calculate(df_current)
    summary_previous = _calculate(df_previous)

    summary_current['total_value_change'] = _get_change(summary_current['total_value'], summary_previous['total_value'])
    summary_current['low_stock_count_change'] = _get_change(summary_current['low_stock_count'], summary_previous['low_stock_count'])
    
    return summary_current

def get_low_stock_items(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Retorna um DataFrame com os itens de estoque baixo."""
    req = {'Nome_Produto', 'Quantidade_Estoque', 'Nivel_Minimo_Estoque'}
    if df is None or df.empty or not req.issubset(df.columns):
        return pd.DataFrame()
        
    dfx = df.copy()
    dfx['gap'] = pd.to_numeric(dfx['Nivel_Minimo_Estoque'], errors='coerce') - \
                 pd.to_numeric(dfx['Quantidade_Estoque'], errors='coerce')
    
    return dfx[dfx['gap'] > 0].sort_values('gap', ascending=False).head(top_n)