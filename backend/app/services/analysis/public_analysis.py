# backend/app/services/analysis/public_analysis.py

import pandas as pd
from typing import Optional

def dist_por_canal(df: pd.DataFrame, ano: Optional[int] = None, mes: Optional[int] = None) -> pd.DataFrame:
    """
    Retorna distribuição de clientes por canal de venda.
    
    Args:
        df: DataFrame com dados de público-alvo
        ano: Ano para filtrar (opcional)
        mes: Mês para filtrar (opcional)
        
    Returns:
        DataFrame com quantidade de clientes por canal
    """
    if df is None or df.empty:
        return pd.DataFrame()
    df_filtered = df.copy()
    if ano is not None:
        df_filtered = df_filtered[df_filtered["Ano"].eq(ano)]
    if mes is not None:
        df_filtered = df_filtered[df_filtered["Mes"].eq(mes)]
    return (df_filtered.groupby("Canal_de_venda", as_index=False)["ID_Cliente"]
              .count().rename(columns={"ID_Cliente": "Qtd_Clientes"}))

def perfil_demografico(df: pd.DataFrame) -> dict:
    """
    Retorna perfil demográfico dos clientes.
    
    Args:
        df: DataFrame com dados de público-alvo
        
    Returns:
        Dicionário com distribuição por gênero e estatísticas de idade
    """
    if df is None or df.empty:
        return {"genero": pd.DataFrame(), "idade_stats": pd.DataFrame()}
    gen = df["Genero"].value_counts().rename_axis("Genero").reset_index(name="Qtd")
    idade = df["Idade"].describe()[["mean","min","max"]].to_frame("Valor").reset_index()
    return {"genero": gen, "idade_stats": idade}

def _get_change(current, previous):
    """Calcula a variação percentual entre dois valores"""
    if previous is None or pd.isna(previous) or previous == 0:
        return None
    return (current - previous) / previous

def analyze_public_kpis(df_current: pd.DataFrame, df_previous: Optional[pd.DataFrame] = None) -> dict:
    """
    Analisa e retorna os KPIs do público-alvo, incluindo a porcentagem do público feminino.
    
    Args:
        df_current: DataFrame com dados do período atual
        df_previous: DataFrame com dados do período anterior (opcional)
        
    Returns:
        Dicionário com KPIs de público-alvo e variações
    """
    def _calculate(df: pd.DataFrame):
        if df is None or df.empty:
            return {'total_clients': 0, 'avg_age': float('nan'), 'avg_spend': float('nan'), 'pct_female': float('nan')}
        
        total_clients = len(df)
        avg_age = pd.to_numeric(df.get('Idade'), errors='coerce').mean()
        gasto_col = 'Gasto_Medio' if 'Gasto_Medio' in df.columns else 'Ticket_Medio'
        avg_spend = pd.to_numeric(df.get(gasto_col), errors='coerce').mean()
        
        pct_female = float('nan')
        if 'Genero' in df.columns and total_clients > 0:
            gender_counts = df['Genero'].astype(str).str.strip().value_counts()
            female_count = gender_counts.get('Feminino', 0)
            pct_female = (female_count / total_clients) * 100

        return {
            'total_clients': total_clients,
            'avg_age': avg_age,
            'avg_spend': avg_spend,
            'pct_female': pct_female
        }

    summary_current = _calculate(df_current)
    summary_previous = _calculate(df_previous)

    summary_current['total_clients_change'] = _get_change(summary_current['total_clients'], summary_previous['total_clients'])

    return summary_current

def get_clients_by_location(df: pd.DataFrame, top_n: int = 10) -> pd.Series:
    """
    Retorna a contagem de clientes por cidade.
    
    Args:
        df: DataFrame com dados de público-alvo
        top_n: Número de cidades a retornar
        
    Returns:
        Series com contagem de clientes por cidade
    """
    location_col = 'Cidade'
    
    if df is None or df.empty or location_col not in df.columns:
        return pd.Series(dtype='object')
        
    return df[location_col].astype(str).value_counts().head(top_n)

def get_clients_by_gender(df: pd.DataFrame) -> pd.Series:
    """
    Retorna a contagem de clientes por gênero.
    
    Args:
        df: DataFrame com dados de público-alvo
        
    Returns:
        Series com contagem por gênero
    """
    if df is None or df.empty or 'Genero' not in df.columns:
        return pd.Series(dtype='object')
    return df['Genero'].astype(str).value_counts()

def get_clients_by_channel(df: pd.DataFrame) -> pd.Series:
    """
    Retorna a contagem de clientes por canal de venda.
    
    Args:
        df: DataFrame com dados de público-alvo
        
    Returns:
        Series com contagem por canal
    """
    if df is None or df.empty or 'Canal_de_venda' not in df.columns:
        return pd.Series(dtype='object')
    return df['Canal_de_venda'].astype(str).value_counts()

