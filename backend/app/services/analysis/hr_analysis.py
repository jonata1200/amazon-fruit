# backend/app/services/analysis/hr_analysis.py

import pandas as pd
from typing import Optional

def _get_change(current, previous):
    """Calcula a variação percentual entre dois valores"""
    if previous is None or pd.isna(previous) or previous == 0:
        return None
    return (current - previous) / previous

def analyze_hr_kpis(df_current: pd.DataFrame, df_previous: Optional[pd.DataFrame] = None) -> dict:
    """
    Analisa e retorna os KPIs de recursos humanos.
    
    Args:
        df_current: DataFrame com dados do período atual
        df_previous: DataFrame com dados do período anterior (opcional)
        
    Returns:
        Dicionário com KPIs de RH e variações
    """
    def _calculate(df: pd.DataFrame):
        if df is None or df.empty:
            return {'total_employees': 0, 'total_monthly_cost': 0.0}
        total_employees = len(df)
        total_monthly_cost = 0.0
        if 'Salario' in df.columns:
            total_monthly_cost = pd.to_numeric(df['Salario'], errors='coerce').fillna(0.0).sum()
        return {'total_employees': total_employees, 'total_monthly_cost': total_monthly_cost}
    
    summary_current = _calculate(df_current)
    summary_previous = _calculate(df_previous)
    summary_current['total_employees_change'] = _get_change(summary_current['total_employees'], summary_previous['total_employees'])
    summary_current['total_monthly_cost_change'] = _get_change(summary_current['total_monthly_cost'], summary_previous['total_monthly_cost'])
    return summary_current

def get_headcount_by_department(df: pd.DataFrame) -> pd.Series:
    """
    Retorna a contagem de funcionários por departamento.
    
    Args:
        df: DataFrame com dados de RH
        
    Returns:
        Series com contagem por departamento
    """
    if df is None or df.empty or 'Departamento' not in df.columns:
        return pd.Series(dtype='object')
    return df['Departamento'].value_counts()

def get_cost_by_department(df: pd.DataFrame) -> pd.Series:
    """
    Retorna a soma dos salários (custo) por departamento.
    
    Args:
        df: DataFrame com dados de RH
        
    Returns:
        Series com custo por departamento
    """
    if df is None or df.empty or not {'Departamento', 'Salario'}.issubset(df.columns):
        return pd.Series(dtype='object')
    return df.groupby('Departamento')['Salario'].sum().sort_values()

def get_headcount_by_role(df: pd.DataFrame) -> pd.Series:
    """
    Retorna a contagem de funcionários por cargo.
    
    Args:
        df: DataFrame com dados de RH
        
    Returns:
        Series com contagem por cargo (top 10)
    """
    if df is None or df.empty or 'Cargo' not in df.columns:
        return pd.Series(dtype='object')
    return df['Cargo'].value_counts().head(10)

def get_hiring_over_time(df: pd.DataFrame) -> pd.Series:
    """
    Retorna a contagem de contratações por mês/ano.
    
    Args:
        df: DataFrame com dados de RH
        
    Returns:
        Series com contagem de contratações por período
    """
    if df is None or df.empty or 'Data_Contratacao' not in df.columns:
        return pd.Series(dtype='object')
    
    df_hiring = df.copy()
    df_hiring['MesAno_Contratacao'] = pd.to_datetime(df_hiring['Data_Contratacao'], errors='coerce').dt.to_period('M').astype(str)
    return df_hiring['MesAno_Contratacao'].value_counts().sort_index()

