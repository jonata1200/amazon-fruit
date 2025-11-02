# modules/analysis/hr_analysis.py
import pandas as pd

def analyze_hr_kpis(df: pd.DataFrame) -> dict:
    """
    Analisa e retorna os KPIs de Recursos Humanos.

    Returns:
        Um dicionário com 'total_employees' e 'total_monthly_cost'.
    """
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