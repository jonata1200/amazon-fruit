# modules/analysis/sales_channel_analysis.py
import pandas as pd

def get_sales_channel_distribution(df: pd.DataFrame) -> pd.Series:
    """Retorna a contagem de clientes por canal de origem."""
    if df is None or df.empty or 'Canal_Origem' not in df.columns:
        return pd.Series(dtype='object')
    return df['Canal_Origem'].astype(str).value_counts()