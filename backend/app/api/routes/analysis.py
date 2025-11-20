# backend/app/api/routes/analysis.py

from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from typing import Optional
import pandas as pd

# Importar DataHandler e módulos de análise
from ...services.data_handler import DataHandler
from ...services.analysis import financial_analysis, inventory_analysis, suppliers_analysis, public_analysis, hr_analysis

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

# Instância global do DataHandler
_data_handler: Optional[DataHandler] = None

def get_data_handler() -> DataHandler:
    """Obtém ou cria uma instância do DataHandler"""
    global _data_handler
    if _data_handler is None:
        project_root = Path(__file__).resolve().parents[4]
        _data_handler = DataHandler(base_dir=project_root)
    return _data_handler

# ============================================================================
# ENDPOINTS DE ANÁLISE FINANCEIRA
# ============================================================================

@router.get("/financial/summary")
async def get_financial_summary(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")
):
    """
    Retorna resumo financeiro (receita, despesa, lucro) e variações percentuais.
    
    Retorna: JSON com valores e variações percentuais comparadas ao período anterior
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        # Carrega dados atual e anterior
        df_current, df_previous = handler.load_comparative_data("Financas")
        
        # Calcula resumo
        summary = financial_analysis.calculate_financial_summary(df_current, df_previous)
        
        # Converte valores None para null (JSON)
        for key, value in summary.items():
            if value is None:
                summary[key] = None
            elif isinstance(value, float) and pd.isna(value):
                summary[key] = None
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular resumo financeiro: {str(e)}")

@router.get("/financial/top-expenses")
async def get_top_expenses(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)"),
    top_n: int = Query(5, ge=1, le=20, description="Número de categorias a retornar")
):
    """
    Retorna top N despesas por categoria.
    
    Retorna: JSON com categorias e valores de despesas
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_fin = handler.load_table("Financas")
        expenses = financial_analysis.get_expense_distribution(df_fin).head(top_n)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "top_n": top_n,
            "data": expenses.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter top despesas: {str(e)}")

@router.get("/financial/top-revenues")
async def get_top_revenues(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)"),
    top_n: int = Query(5, ge=1, le=20, description="Número de categorias a retornar")
):
    """
    Retorna top N receitas por categoria.
    
    Retorna: JSON com categorias e valores de receitas
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_fin = handler.load_table("Financas")
        revenues = financial_analysis.get_revenue_distribution(df_fin, top_n=top_n)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "top_n": top_n,
            "data": revenues.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter top receitas: {str(e)}")

# ============================================================================
# ENDPOINTS DE ANÁLISE DE ESTOQUE
# ============================================================================

@router.get("/inventory/top-selling")
async def get_top_selling_items(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)"),
    top_n: int = Query(10, ge=1, le=50, description="Número de produtos a retornar")
):
    """
    Retorna top N produtos mais vendidos por faturamento.
    
    Retorna: JSON com produtos e faturamento total
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_fin = handler.load_table("Financas")
        df_estoque = handler.load_table("Estoque")
        
        top_selling = financial_analysis.get_top_selling_items(df_fin, df_estoque, top_n=top_n)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "top_n": top_n,
            "data": top_selling.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter top produtos: {str(e)}")

@router.get("/inventory/low-stock")
async def get_low_stock_items(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)"),
    top_n: int = Query(10, ge=1, le=50, description="Número de produtos a retornar")
):
    """
    Retorna produtos com estoque baixo (rupturas).
    
    Retorna: JSON com produtos e gap de estoque
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_estoque = handler.load_table("Estoque")
        low_stock = inventory_analysis.get_low_stock_items(df_estoque, top_n=top_n)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "top_n": top_n,
            "data": low_stock.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter produtos com estoque baixo: {str(e)}")

@router.get("/inventory/kpis")
async def get_inventory_kpis(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")
):
    """
    Retorna KPIs de estoque (produtos únicos, valor total, itens com estoque baixo).
    
    Retorna: JSON com KPIs e variações percentuais
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_current, df_previous = handler.load_comparative_data("Estoque")
        kpis = inventory_analysis.analyze_inventory_kpis(df_current, df_previous)
        
        # Converte valores None para null
        for key, value in kpis.items():
            if value is None:
                kpis[key] = None
            elif isinstance(value, float) and pd.isna(value):
                kpis[key] = None
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "kpis": kpis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular KPIs de estoque: {str(e)}")

# ============================================================================
# ENDPOINTS DE ANÁLISE DE FORNECEDORES
# ============================================================================

@router.get("/suppliers/top-bottom")
async def get_top_bottom_suppliers(
    n: int = Query(5, ge=1, le=20, description="Número de fornecedores em cada categoria")
):
    """
    Retorna top N melhores e piores fornecedores por avaliação.
    
    Retorna: JSON com fornecedores top e bottom
    """
    try:
        handler = get_data_handler()
        df_fornecedores = handler.load_full_unfiltered_table("Fornecedores")
        
        result = suppliers_analysis.get_top_bottom_suppliers(df_fornecedores, n=n)
        
        return {
            "status": "success",
            "n": n,
            "top": result['top'].to_dict(orient='records'),
            "bottom": result['bottom'].to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter ranking de fornecedores: {str(e)}")

@router.get("/suppliers/by-state")
async def get_suppliers_by_state():
    """
    Retorna distribuição de fornecedores por estado.
    
    Retorna: JSON com contagem de fornecedores por estado
    """
    try:
        handler = get_data_handler()
        df_fornecedores = handler.load_full_unfiltered_table("Fornecedores")
        
        by_state = suppliers_analysis.get_suppliers_by_state(df_fornecedores)
        
        return {
            "status": "success",
            "data": by_state.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter distribuição por estado: {str(e)}")

# ============================================================================
# ENDPOINTS DE ANÁLISE DE PÚBLICO-ALVO
# ============================================================================

@router.get("/public/by-location")
async def get_clients_by_location(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)"),
    top_n: int = Query(10, ge=1, le=50, description="Número de localizações a retornar")
):
    """
    Retorna top N clientes por localização (cidade).
    
    Retorna: JSON com contagem de clientes por cidade
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_publico = handler.load_table("Publico_Alvo")
        by_location = public_analysis.get_clients_by_location(df_publico, top_n=top_n)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "top_n": top_n,
            "data": by_location.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter clientes por localização: {str(e)}")

@router.get("/public/by-gender")
async def get_clients_by_gender(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")
):
    """
    Retorna distribuição de clientes por gênero.
    
    Retorna: JSON com contagem por gênero
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_publico = handler.load_table("Publico_Alvo")
        by_gender = public_analysis.get_clients_by_gender(df_publico)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "data": by_gender.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter distribuição por gênero: {str(e)}")

@router.get("/public/by-channel")
async def get_clients_by_channel(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")
):
    """
    Retorna contagem de clientes por canal de venda.
    
    Retorna: JSON com contagem por canal
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_publico = handler.load_table("Publico_Alvo")
        by_channel = public_analysis.get_clients_by_channel(df_publico)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "data": by_channel.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter distribuição por canal: {str(e)}")

# ============================================================================
# ENDPOINTS DE ANÁLISE DE RECURSOS HUMANOS
# ============================================================================

@router.get("/hr/by-department")
async def get_headcount_by_department():
    """
    Retorna número de funcionários por departamento.
    
    Retorna: JSON com contagem por departamento
    """
    try:
        handler = get_data_handler()
        df_rh = handler.load_full_unfiltered_table("Recursos_Humanos")
        
        headcount = hr_analysis.get_headcount_by_department(df_rh)
        
        return {
            "status": "success",
            "data": headcount.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter headcount por departamento: {str(e)}")

@router.get("/hr/cost-by-department")
async def get_cost_by_department():
    """
    Retorna custo mensal por departamento.
    
    Retorna: JSON com custo total por departamento
    """
    try:
        handler = get_data_handler()
        df_rh = handler.load_full_unfiltered_table("Recursos_Humanos")
        
        costs = hr_analysis.get_cost_by_department(df_rh)
        
        return {
            "status": "success",
            "data": costs.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter custos por departamento: {str(e)}")

@router.get("/hr/by-role")
async def get_headcount_by_role():
    """
    Retorna top 10 cargos na empresa.
    
    Retorna: JSON com contagem por cargo
    """
    try:
        handler = get_data_handler()
        df_rh = handler.load_full_unfiltered_table("Recursos_Humanos")
        
        roles = hr_analysis.get_headcount_by_role(df_rh)
        
        return {
            "status": "success",
            "data": roles.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter distribuição por cargo: {str(e)}")

@router.get("/hr/hiring-over-time")
async def get_hiring_over_time():
    """
    Retorna histórico de contratações ao longo do tempo.
    
    Retorna: JSON com contagem de contratações por período
    """
    try:
        handler = get_data_handler()
        df_rh = handler.load_full_unfiltered_table("Recursos_Humanos")
        
        hiring = hr_analysis.get_hiring_over_time(df_rh)
        
        return {
            "status": "success",
            "data": hiring.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter histórico de contratações: {str(e)}")

