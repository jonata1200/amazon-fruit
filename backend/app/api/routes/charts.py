# backend/app/api/routes/charts.py

from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from typing import Optional

# Importar DataHandler e funções de gráficos
from ...services.data_handler import DataHandler
from ...services.charts.chart_generator import (
    create_general_evolution_chart_data,
    create_finance_evolution_chart_data,
    create_top_expenses_chart_data,
    create_top_revenues_chart_data,
    create_top_selling_chart_data,
    create_least_selling_chart_data,
    create_stock_rupture_chart_data,
    create_supplier_ranking_chart_data,
    create_supplier_geo_chart_data,
    create_public_location_chart_data,
    create_public_gender_chart_data,
    create_public_channel_chart_data,
    create_hr_headcount_chart_data,
    create_hr_cost_chart_data,
    create_hr_role_chart_data,
    create_hr_hiring_chart_data
)

router = APIRouter(prefix="/api/charts", tags=["charts"])

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
# GRÁFICOS FINANCEIROS
# ============================================================================

@router.get("/financial/evolution")
async def get_financial_evolution_chart(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")
):
    """
    Retorna dados formatados para gráfico de evolução financeira (Plotly).
    
    Retorna: JSON com estrutura Plotly para renderização no frontend
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_fin = handler.load_table("Financas")
        chart_data = create_finance_evolution_chart_data(df_fin)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

@router.get("/financial/top-expenses")
async def get_top_expenses_chart(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)"),
    top_n: int = Query(5, ge=1, le=20)
):
    """Retorna gráfico de top despesas (Plotly)"""
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_fin = handler.load_table("Financas")
        chart_data = create_top_expenses_chart_data(df_fin, top_n=top_n)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

@router.get("/financial/top-revenues")
async def get_top_revenues_chart(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)"),
    top_n: int = Query(5, ge=1, le=20)
):
    """Retorna gráfico de top receitas (Plotly)"""
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_fin = handler.load_table("Financas")
        chart_data = create_top_revenues_chart_data(df_fin, top_n=top_n)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

# ============================================================================
# GRÁFICOS DE ESTOQUE
# ============================================================================

@router.get("/inventory/top-selling")
async def get_top_selling_chart(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)"),
    top_n: int = Query(10, ge=1, le=50)
):
    """Retorna gráfico de top produtos vendidos (Plotly)"""
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_fin = handler.load_table("Financas")
        df_estoque = handler.load_full_unfiltered_table("Estoque")
        
        chart_data = create_top_selling_chart_data(df_fin, df_estoque, top_n=top_n)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

@router.get("/inventory/stock-rupture")
async def get_stock_rupture_chart(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)"),
    top_n: int = Query(10, ge=1, le=50)
):
    """Retorna gráfico de rupturas de estoque (Plotly)"""
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_estoque = handler.load_table("Estoque")
        chart_data = create_stock_rupture_chart_data(df_estoque, top_n=top_n)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

# ============================================================================
# GRÁFICOS DE FORNECEDORES
# ============================================================================

@router.get("/suppliers/ranking")
async def get_supplier_ranking_chart(
    n: int = Query(5, ge=1, le=20)
):
    """Retorna gráfico de ranking de fornecedores (Plotly)"""
    try:
        handler = get_data_handler()
        df_fornecedores = handler.load_full_unfiltered_table("Fornecedores")
        
        chart_data = create_supplier_ranking_chart_data(df_fornecedores, n=n)
        
        return {
            "status": "success",
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

@router.get("/suppliers/by-state")
async def get_suppliers_by_state_chart():
    """Retorna gráfico de distribuição de fornecedores por estado (Plotly)"""
    try:
        handler = get_data_handler()
        df_fornecedores = handler.load_full_unfiltered_table("Fornecedores")
        
        chart_data = create_supplier_geo_chart_data(df_fornecedores)
        
        return {
            "status": "success",
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

# ============================================================================
# GRÁFICOS DE PÚBLICO-ALVO
# ============================================================================

@router.get("/public/location")
async def get_public_location_chart(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)"),
    top_n: int = Query(10, ge=1, le=50)
):
    """Retorna gráfico de clientes por localização (Plotly)"""
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_publico = handler.load_table("Publico_Alvo")
        chart_data = create_public_location_chart_data(df_publico, top_n=top_n)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

@router.get("/public/gender")
async def get_public_gender_chart(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")
):
    """Retorna gráfico de distribuição por gênero (Plotly)"""
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_publico = handler.load_table("Publico_Alvo")
        chart_data = create_public_gender_chart_data(df_publico)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

@router.get("/public/channel")
async def get_public_channel_chart(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")
):
    """Retorna gráfico de distribuição por canal (Plotly)"""
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_publico = handler.load_table("Publico_Alvo")
        chart_data = create_public_channel_chart_data(df_publico)
        
        return {
            "status": "success",
            "period": {"start": start_date, "end": end_date},
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

# ============================================================================
# GRÁFICOS DE RECURSOS HUMANOS
# ============================================================================

@router.get("/hr/headcount")
async def get_hr_headcount_chart():
    """Retorna gráfico de headcount por departamento (Plotly)"""
    try:
        handler = get_data_handler()
        df_rh = handler.load_full_unfiltered_table("Recursos_Humanos")
        
        chart_data = create_hr_headcount_chart_data(df_rh)
        
        return {
            "status": "success",
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

@router.get("/hr/cost")
async def get_hr_cost_chart():
    """Retorna gráfico de custo por departamento (Plotly)"""
    try:
        handler = get_data_handler()
        df_rh = handler.load_full_unfiltered_table("Recursos_Humanos")
        
        chart_data = create_hr_cost_chart_data(df_rh)
        
        return {
            "status": "success",
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

@router.get("/hr/role")
async def get_hr_role_chart():
    """Retorna gráfico de distribuição por cargo (Plotly)"""
    try:
        handler = get_data_handler()
        df_rh = handler.load_full_unfiltered_table("Recursos_Humanos")
        
        chart_data = create_hr_role_chart_data(df_rh)
        
        return {
            "status": "success",
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

@router.get("/hr/hiring")
async def get_hr_hiring_chart():
    """Retorna gráfico de histórico de contratações (Plotly)"""
    try:
        handler = get_data_handler()
        df_rh = handler.load_full_unfiltered_table("Recursos_Humanos")
        
        chart_data = create_hr_hiring_chart_data(df_rh)
        
        return {
            "status": "success",
            "chart": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

