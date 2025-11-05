# modules/analysis/hr_analysis.py

from modules.utils.data_handler import DataRepository
import pandas as pd

repo = DataRepository()

def headcount_por_departamento():
    df = repo.load_rh()
    return df.groupby("Departamento", as_index=False)["ID_Funcionario"].count() \
             .rename(columns={"ID_Funcionario":"Headcount"})

def massa_salarial():
    df = repo.load_rh()
    return df["Salario"].sum()

def _get_change(current, previous):
    if previous is None or pd.isna(previous) or previous == 0:
        return None
    return (current - previous) / previous

def analyze_hr_kpis(df_current: pd.DataFrame, df_previous: pd.DataFrame = None) -> dict:
    """Analisa e retorna os KPIs de RH para o período atual e a variação."""

    def _calculate(df: pd.DataFrame):
        if df is None or df.empty:
            return {'total_employees': 0, 'total_monthly_cost': 0.0}
            
        total_employees = len(df)
        
        total_monthly_cost = 0.0
        if 'Salario' in df.columns:
            total_monthly_cost = pd.to_numeric(df['Salario'], errors='coerce').fillna(0.0).sum()
            
        return {
            'total_employees': total_employees,
            'total_monthly_cost': total_monthly_cost
        }
    
    summary_current = _calculate(df_current)
    summary_previous = _calculate(df_previous)
    
    summary_current['total_employees_change'] = _get_change(summary_current['total_employees'], summary_previous['total_employees'])
    summary_current['total_monthly_cost_change'] = _get_change(summary_current['total_monthly_cost'], summary_previous['total_monthly_cost'])

    return summary_current