# modules/analysis/public_analysis.py
import pandas as pd

def analyze_public_kpis(df: pd.DataFrame) -> dict:
    """Analisa e retorna os KPIs do público-alvo."""
    if df is None or df.empty:
        return {'total_clients': 0, 'avg_age': float('nan'), 'avg_spend': float('nan')}
        
    total_clients = len(df)
    
    avg_age = pd.to_numeric(df.get('Idade'), errors='coerce').mean()
    
    gasto_col = 'Gasto_Medio' if 'Gasto_Medio' in df.columns else 'Ticket_Medio'
    avg_spend = pd.to_numeric(df.get(gasto_col), errors='coerce').mean()
    
    return {
        'total_clients': total_clients,
        'avg_age': avg_age,
        'avg_spend': avg_spend
    }

def get_clients_by_location(df: pd.DataFrame, top_n: int = 10) -> pd.Series:
    """Retorna a contagem de clientes por localização."""
    if df is None or df.empty or 'Localizacao' not in df.columns:
        return pd.Series(dtype='object')
    return df['Localizacao'].astype(str).value_counts().head(top_n)

def get_clients_by_gender(df: pd.DataFrame) -> pd.Series:
    """Retorna a contagem de clientes por gênero."""
    if df is None or df.empty or 'Genero' not in df.columns:
        return pd.Series(dtype='object')
    return df['Genero'].astype(str).value_counts()