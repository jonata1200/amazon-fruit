# modules/analysis/public_analysis.py

import pandas as pd

def dist_por_canal(df: pd.DataFrame, ano:int|None=None, mes:int|None=None):
    # A função agora recebe o DataFrame em vez de carregá-lo.
    if df is None or df.empty:
        return pd.DataFrame()
    if ano is not None: df = df[df["Ano"].eq(ano)]
    if mes is not None: df = df[df["Mes"].eq(mes)]
    return (df.groupby("Canal_de_venda", as_index=False)["ID_Cliente"]
              .count().rename(columns={"ID_Cliente":"Qtd_Clientes"}))

def perfil_demografico(df: pd.DataFrame):
    # A função agora recebe o DataFrame em vez de carregá-lo.
    if df is None or df.empty:
        return {"genero": pd.DataFrame(), "idade_stats": pd.DataFrame()}
    gen = df["Genero"].value_counts().rename_axis("Genero").reset_index(name="Qtd")
    idade = df["Idade"].describe()[["mean","min","max"]].to_frame("Valor").reset_index()
    return {"genero": gen, "idade_stats": idade}

def _get_change(current, previous):
    if previous is None or pd.isna(previous) or previous == 0:
        return None
    return (current - previous) / previous

def analyze_public_kpis(df_current: pd.DataFrame, df_previous: pd.DataFrame = None) -> dict:
    """
    Analisa e retorna os KPIs do público-alvo, agora incluindo
    a porcentagem do público feminino.
    """

    def _calculate(df: pd.DataFrame):
        if df is None or df.empty:
            return {'total_clients': 0, 'avg_age': float('nan'), 'avg_spend': float('nan'), 'pct_female': float('nan')}
        
        total_clients = len(df)
        avg_age = pd.to_numeric(df.get('Idade'), errors='coerce').mean()
        gasto_col = 'Gasto_Medio' if 'Gasto_Medio' in df.columns else 'Ticket_Medio'
        avg_spend = pd.to_numeric(df.get(gasto_col), errors='coerce').mean()
        
        # --- NOVA LÓGICA ADICIONADA AQUI ---
        pct_female = float('nan')
        if 'Genero' in df.columns and total_clients > 0:
            gender_counts = df['Genero'].astype(str).str.strip().value_counts()
            female_count = gender_counts.get('Feminino', 0)
            # Calcula a porcentagem, evitando divisão por zero
            pct_female = (female_count / total_clients) * 100
        # --- FIM DA NOVA LÓGICA ---

        return {
            'total_clients': total_clients,
            'avg_age': avg_age,
            'avg_spend': avg_spend,
            'pct_female': pct_female # Adiciona o novo KPI ao resultado
        }

    summary_current = _calculate(df_current)
    summary_previous = _calculate(df_previous)

    summary_current['total_clients_change'] = _get_change(summary_current['total_clients'], summary_previous['total_clients'])

    return summary_current

def get_clients_by_location(df: pd.DataFrame, top_n: int = 10) -> pd.Series:
    """Retorna a contagem de clientes por cidade (a coluna de localização nos dados)."""
    location_col = 'Cidade'
    
    if df is None or df.empty or location_col not in df.columns:
        return pd.Series(dtype='object')
        
    return df[location_col].astype(str).value_counts().head(top_n)

def get_clients_by_gender(df: pd.DataFrame) -> pd.Series:
    """Retorna a contagem de clientes por gênero."""
    if df is None or df.empty or 'Genero' not in df.columns:
        return pd.Series(dtype='object')
    return df['Genero'].astype(str).value_counts()

def get_clients_by_channel(df: pd.DataFrame) -> pd.Series:
    """Retorna a contagem de clientes por canal de venda."""
    if df is None or df.empty or 'Canal_de_venda' not in df.columns:
        return pd.Series(dtype='object')
    return df['Canal_de_venda'].astype(str).value_counts()