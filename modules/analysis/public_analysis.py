# modules/analysis/public_analysis.py
import pandas as pd
from modules.utils.data_handler import DataRepository

repo = DataRepository()

def dist_por_canal(ano:int|None=None, mes:int|None=None):
    df = repo.load_publico_alvo()
    if ano is not None: df = df[df["Ano"].eq(ano)]
    if mes is not None: df = df[df["Mes"].eq(mes)]
    return (df.groupby("Canal_de_venda", as_index=False)["ID_Cliente"]
              .count().rename(columns={"ID_Cliente":"Qtd_Clientes"}))

def perfil_demografico():
    df = repo.load_publico_alvo()
    gen = df["Genero"].value_counts().rename_axis("Genero").reset_index(name="Qtd")
    idade = df["Idade"].describe()[["mean","min","max"]].to_frame("Valor").reset_index()
    return {"genero": gen, "idade_stats": idade}

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