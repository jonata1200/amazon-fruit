# backend/app/api/routes/alerts.py

from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from typing import Optional, List, Dict
import pandas as pd

# Importar DataHandler e módulos de análise
from ...services.data_handler import DataHandler
from ...services.analysis import inventory_analysis, financial_analysis
from ...utils.validators import validate_date_range

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

# Instância global do DataHandler
_data_handler: Optional[DataHandler] = None

def get_data_handler() -> DataHandler:
    """Obtém ou cria uma instância do DataHandler"""
    global _data_handler
    if _data_handler is None:
        project_root = Path(__file__).resolve().parents[4]
        _data_handler = DataHandler(base_dir=project_root)
    return _data_handler

@router.get("/")
async def get_all_alerts(
    start_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)")
):
    # Validar datas se fornecidas
    if start_date and end_date:
        start_date, end_date = validate_date_range(start_date, end_date)
    """
    Retorna todos os alertas ativos do sistema.
    
    Tipos de alertas:
    - Estoque baixo
    - Despesas acima do esperado
    - Receitas abaixo da meta
    - Lucro negativo
    """
    try:
        handler = get_data_handler()
        
        alerts = []
        
        # Se datas foram fornecidas, configura o período
        if start_date and end_date:
            handler.set_period(start_date, end_date)
        
        # 1. Alertas de Estoque Baixo
        try:
            inventory_alerts = get_inventory_alerts(handler, start_date, end_date)
            alerts.extend(inventory_alerts)
        except Exception as e:
            print(f"Erro ao obter alertas de estoque: {e}")
        
        # 2. Alertas Financeiros
        try:
            financial_alerts = get_financial_alerts(handler, start_date, end_date)
            alerts.extend(financial_alerts)
        except Exception as e:
            print(f"Erro ao obter alertas financeiros: {e}")
        
        return {
            "status": "success",
            "count": len(alerts),
            "alerts": alerts
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter alertas: {str(e)}")

@router.get("/inventory")
async def get_inventory_alerts_endpoint(
    start_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)")
):
    """
    Retorna alertas de estoque baixo.
    """
    try:
        handler = get_data_handler()
        
        if start_date and end_date:
            start_date, end_date = validate_date_range(start_date, end_date)
            handler.set_period(start_date, end_date)
        
        alerts_list = get_inventory_alerts(handler, start_date, end_date)
        
        return {
            "status": "success",
            "count": len(alerts_list),
            "alerts": alerts_list
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter alertas de estoque: {str(e)}")

@router.get("/financial")
async def get_financial_alerts_endpoint(
    start_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)")
):
    """
    Retorna alertas financeiros.
    """
    try:
        handler = get_data_handler()
        
        if start_date and end_date:
            start_date, end_date = validate_date_range(start_date, end_date)
            handler.set_period(start_date, end_date)
        
        alerts_list = get_financial_alerts(handler, start_date, end_date)
        
        return {
            "status": "success",
            "count": len(alerts_list),
            "alerts": alerts_list
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter alertas financeiros: {str(e)}")

# Funções auxiliares

def get_inventory_alerts(handler: DataHandler, start_date: Optional[str], end_date: Optional[str]) -> List[Dict]:
    """Obtém alertas de estoque baixo"""
    alerts = []
    
    try:
        # Carregar dados de estoque
        df_estoque = handler.load_table("Estoque")
        
        if df_estoque is None or df_estoque.empty:
            return alerts
        
        # Obter produtos com estoque baixo
        low_stock_df = inventory_analysis.get_low_stock_items(df_estoque, top_n=10)
        
        if not low_stock_df.empty:
            # Converter DataFrame para lista de dicionários
            for _, row in low_stock_df.iterrows():
                produto = row.get('Produto', 'N/A')
                quantidade = row.get('Quantidade_Estoque', 0)
                nivel_minimo = row.get('Nivel_Minimo_Estoque', 0)
                
                alerts.append({
                    "type": "inventory_low",
                    "severity": "warning",
                    "title": "Estoque Baixo",
                    "message": f"Produto '{produto}' está com estoque baixo ({quantidade} unidades, mínimo: {nivel_minimo})",
                    "product": produto,
                    "current_stock": int(quantidade) if pd.notna(quantidade) else 0,
                    "min_stock": int(nivel_minimo) if pd.notna(nivel_minimo) else 0,
                    "dashboard": "estoque"
                })
    except Exception as e:
        print(f"Erro ao processar alertas de estoque: {e}")
    
    return alerts

def get_financial_alerts(handler: DataHandler, start_date: Optional[str], end_date: Optional[str]) -> List[Dict]:
    """Obtém alertas financeiros"""
    alerts = []
    
    try:
        if not start_date or not end_date:
            return alerts
        
        # Carregar dados financeiros
        df_financas = handler.load_table("Financas")
        
        if df_financas is None or df_financas.empty:
            return alerts
        
        # Obter resumo financeiro (sem período anterior para alertas)
        summary = financial_analysis.calculate_financial_summary(df_financas, None)
        
        if summary:
            receita = summary.get('receita', 0)
            despesa = summary.get('despesa', 0)
            lucro = summary.get('lucro', 0)
            
            # Alertar se lucro negativo
            if lucro < 0:
                alerts.append({
                    "type": "negative_profit",
                    "severity": "danger",
                    "title": "Lucro Negativo",
                    "message": f"O lucro está negativo no período: R$ {lucro:,.2f}",
                    "value": float(lucro),
                    "dashboard": "financas"
                })
            
            # Alertar se despesa > 80% da receita
            if receita > 0:
                expense_ratio = despesa / receita
                if expense_ratio > 0.8:
                    alerts.append({
                        "type": "high_expenses",
                        "severity": "warning",
                        "title": "Despesas Elevadas",
                        "message": f"Despesas representam {expense_ratio*100:.1f}% da receita",
                        "ratio": float(expense_ratio),
                        "dashboard": "financas"
                    })
            
            # Alertar se receita muito baixa (menor que despesa * 1.1)
            if receita > 0 and despesa > 0 and receita < despesa * 1.1:
                alerts.append({
                    "type": "low_revenue",
                    "severity": "warning",
                    "title": "Receita Baixa",
                    "message": f"Receita está apenas {(receita/despesa*100):.1f}% acima das despesas",
                    "revenue": float(receita),
                    "expenses": float(despesa),
                    "dashboard": "financas"
                })
                
    except Exception as e:
        print(f"Erro ao processar alertas financeiros: {e}")
    
    return alerts

