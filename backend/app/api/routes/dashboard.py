# backend/app/api/routes/dashboard.py

from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from typing import Optional
import pandas as pd

# Importar DataHandler e módulos de análise
from ...services.data_handler import DataHandler
from ...services.analysis import financial_analysis, inventory_analysis, suppliers_analysis, public_analysis, hr_analysis

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

# Instância global do DataHandler
_data_handler: Optional[DataHandler] = None

def get_data_handler() -> DataHandler:
    """Obtém ou cria uma instância do DataHandler"""
    global _data_handler
    if _data_handler is None:
        project_root = Path(__file__).resolve().parents[4]
        _data_handler = DataHandler(base_dir=project_root)
    return _data_handler

@router.get("/geral")
async def get_dashboard_geral(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")
):
    """
    Retorna todos os dados necessários para o dashboard geral.
    
    Inclui:
    - Resumo financeiro (receita, despesa, lucro)
    - Dados para gráfico de evolução mensal
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        # Carrega dados financeiros
        df_fin_current, df_fin_previous = handler.load_comparative_data("Financas")
        
        # Calcula resumo financeiro
        financial_summary = financial_analysis.calculate_financial_summary(df_fin_current, df_fin_previous)
        
        # Prepara dados para gráfico de evolução mensal
        evolution_data = {}
        if not df_fin_current.empty and 'Data' in df_fin_current.columns:
            df_fin_copy = df_fin_current.copy()
            df_fin_copy['MesAno'] = pd.to_datetime(df_fin_copy['Data'], errors='coerce').dt.to_period('M').astype(str)
            monthly = df_fin_copy.groupby(['MesAno', 'Tipo'])['Valor'].sum().unstack(fill_value=0)
            
            if 'Receita' not in monthly.columns:
                monthly['Receita'] = 0
            if 'Despesa' not in monthly.columns:
                monthly['Despesa'] = 0
                
            monthly['Lucro'] = monthly['Receita'] - monthly['Despesa']
            
            evolution_data = {
                "months": monthly.index.tolist(),
                "receita": monthly['Receita'].tolist(),
                "despesa": monthly['Despesa'].tolist(),
                "lucro": monthly['Lucro'].tolist()
            }
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "financial_summary": financial_summary,
            "evolution_chart": evolution_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dashboard geral: {str(e)}")

@router.get("/financas")
async def get_dashboard_financas(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")
):
    """
    Retorna dados do dashboard de finanças.
    
    Inclui:
    - Resumo financeiro
    - Top 5 despesas
    - Top 5 receitas
    - Dados para gráfico de evolução
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_fin_current, df_fin_previous = handler.load_comparative_data("Financas")
        
        # Resumo financeiro
        financial_summary = financial_analysis.calculate_financial_summary(df_fin_current, df_fin_previous)
        
        # Top despesas e receitas
        top_expenses = financial_analysis.get_expense_distribution(df_fin_current).head(5)
        top_revenues = financial_analysis.get_revenue_distribution(df_fin_current, top_n=5)
        
        # Dados para gráfico de evolução
        evolution_data = {}
        if not df_fin_current.empty and 'Data' in df_fin_current.columns:
            df_fin_copy = df_fin_current.copy()
            df_fin_copy['MesAno'] = pd.to_datetime(df_fin_copy['Data'], errors='coerce').dt.to_period('M').astype(str)
            monthly = df_fin_copy.groupby(['MesAno', 'Tipo'])['Valor'].sum().unstack(fill_value=0)
            
            if 'Receita' not in monthly.columns:
                monthly['Receita'] = 0
            if 'Despesa' not in monthly.columns:
                monthly['Despesa'] = 0
                
            monthly['Lucro'] = monthly['Receita'] - monthly['Despesa']
            
            evolution_data = {
                "months": monthly.index.tolist(),
                "receita": monthly['Receita'].tolist(),
                "despesa": monthly['Despesa'].tolist(),
                "lucro": monthly['Lucro'].tolist()
            }
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "financial_summary": financial_summary,
            "top_expenses": top_expenses.to_dict(),
            "top_revenues": top_revenues.to_dict(),
            "evolution_chart": evolution_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dashboard de finanças: {str(e)}")

@router.get("/estoque")
async def get_dashboard_estoque(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")
):
    """
    Retorna dados do dashboard de estoque.
    
    Inclui:
    - KPIs de estoque
    - Top produtos vendidos
    - Produtos menos vendidos
    - Produtos com estoque baixo
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_fin = handler.load_table("Financas")
        df_estoque_current, df_estoque_previous = handler.load_comparative_data("Estoque")
        df_estoque_full = handler.load_full_unfiltered_table("Estoque")
        
        # KPIs
        kpis = inventory_analysis.analyze_inventory_kpis(df_estoque_current, df_estoque_previous)
        
        # Top produtos
        top_selling = financial_analysis.get_top_selling_items(df_fin, df_estoque_full, top_n=10)
        least_selling = financial_analysis.get_least_selling_items(df_fin, df_estoque_full, top_n=10)
        
        # Estoque baixo
        low_stock = inventory_analysis.get_low_stock_items(df_estoque_current, top_n=10)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "kpis": kpis,
            "top_selling": top_selling.to_dict(),
            "least_selling": least_selling.to_dict(),
            "low_stock": low_stock.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dashboard de estoque: {str(e)}")

@router.get("/publico_alvo")
async def get_dashboard_publico_alvo(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")
):
    """
    Retorna dados do dashboard de público-alvo.
    
    Inclui:
    - Clientes por localização
    - Distribuição por gênero
    - Distribuição por canal
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_publico = handler.load_table("Publico_Alvo")
        
        by_location = public_analysis.get_clients_by_location(df_publico, top_n=10)
        by_gender = public_analysis.get_clients_by_gender(df_publico)
        by_channel = public_analysis.get_clients_by_channel(df_publico)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "by_location": by_location.to_dict(),
            "by_gender": by_gender.to_dict(),
            "by_channel": by_channel.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dashboard de público-alvo: {str(e)}")

@router.get("/fornecedores")
async def get_dashboard_fornecedores():
    """
    Retorna dados do dashboard de fornecedores.
    
    Inclui:
    - Top e bottom fornecedores
    - Distribuição por estado
    """
    try:
        handler = get_data_handler()
        df_fornecedores = handler.load_full_unfiltered_table("Fornecedores")
        
        top_bottom = suppliers_analysis.get_top_bottom_suppliers(df_fornecedores, n=5)
        by_state = suppliers_analysis.get_suppliers_by_state(df_fornecedores)
        
        return {
            "status": "success",
            "top_suppliers": top_bottom['top'].to_dict(orient='records'),
            "bottom_suppliers": top_bottom['bottom'].to_dict(orient='records'),
            "by_state": by_state.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dashboard de fornecedores: {str(e)}")

@router.get("/recursos_humanos")
async def get_dashboard_recursos_humanos():
    """
    Retorna dados do dashboard de recursos humanos.
    
    Inclui:
    - Headcount por departamento
    - Custo por departamento
    - Distribuição por cargo
    - Histórico de contratações
    """
    try:
        handler = get_data_handler()
        df_rh = handler.load_full_unfiltered_table("Recursos_Humanos")
        
        headcount = hr_analysis.get_headcount_by_department(df_rh)
        costs = hr_analysis.get_cost_by_department(df_rh)
        roles = hr_analysis.get_headcount_by_role(df_rh)
        hiring = hr_analysis.get_hiring_over_time(df_rh)
        
        return {
            "status": "success",
            "headcount_by_department": headcount.to_dict(),
            "cost_by_department": costs.to_dict(),
            "by_role": roles.to_dict(),
            "hiring_over_time": hiring.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dashboard de RH: {str(e)}")

