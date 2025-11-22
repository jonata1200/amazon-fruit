# backend/app/api/routes/export.py

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pathlib import Path
from typing import Optional
import pandas as pd
import io
from datetime import datetime

# Importação relativa do DataHandler
from ...services.data_handler import DataHandler

router = APIRouter(prefix="/api/export", tags=["export"])

# Instância global do DataHandler
_data_handler: Optional[DataHandler] = None

def get_data_handler() -> DataHandler:
    """Obtém ou cria uma instância do DataHandler"""
    global _data_handler
    if _data_handler is None:
        project_root = Path(__file__).resolve().parents[4]
        _data_handler = DataHandler(base_dir=project_root)
    return _data_handler

@router.get("/{table_name}")
async def export_table(
    table_name: str,
    format: str = Query("xlsx", description="Formato de exportação: xlsx ou csv"),
    start_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)")
):
    """
    Exporta dados de uma tabela para Excel (.xlsx) ou CSV.
    
    Parâmetros:
    - table_name: Nome da tabela (financas, estoque, publico_alvo, fornecedores, recursos_humanos)
    - format: Formato de exportação (xlsx ou csv) - padrão: xlsx
    - start_date: Data inicial no formato ISO (YYYY-MM-DD) - opcional
    - end_date: Data final no formato ISO (YYYY-MM-DD) - opcional
    
    Retorna: Arquivo para download
    """
    try:
        handler = get_data_handler()
        
        # Validar formato
        format = format.lower()
        if format not in ['xlsx', 'csv']:
            raise HTTPException(status_code=400, detail="Formato inválido. Use 'xlsx' ou 'csv'")
        
        # Carregar dados
        table_key = table_name.lower().replace('_', '')
        
        if table_key in ['publicoalvo', 'fornecedores']:
            # Carrega todos os dados (sem filtro de data)
            df = handler.load_full_unfiltered_table(table_name)
        else:
            # Se datas foram fornecidas, configura o período
            if start_date and end_date:
                handler.set_period(start_date, end_date)
            # Carrega os dados com filtro de data
            df = handler.load_table(table_name)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para exportar")
        
        # Gerar nome do arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        date_suffix = ""
        if start_date and end_date:
            date_suffix = f"_{start_date}_{end_date}"
        filename = f"{table_name}{date_suffix}_{timestamp}.{format}"
        
        # Criar arquivo em memória
        output = io.BytesIO()
        
        if format == 'xlsx':
            # Exportar para Excel
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Dados')
            
            output.seek(0)
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
        else:  # CSV
            # Exportar para CSV
            df.to_csv(output, index=False, encoding='utf-8-sig')  # utf-8-sig para Excel reconhecer acentos
            output.seek(0)
            media_type = "text/csv"
        
        # Retornar arquivo para download
        return StreamingResponse(
            io.BytesIO(output.read()),
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Banco de dados não encontrado: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar dados: {str(e)}")

@router.get("/dashboard/{dashboard_name}")
async def export_dashboard_data(
    dashboard_name: str,
    format: str = Query("xlsx", description="Formato de exportação: xlsx ou csv"),
    start_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)")
):
    """
    Exporta todos os dados de um dashboard específico.
    
    Parâmetros:
    - dashboard_name: Nome do dashboard (geral, financas, estoque, publico_alvo, fornecedores, recursos_humanos)
    - format: Formato de exportação (xlsx ou csv) - padrão: xlsx
    - start_date: Data inicial no formato ISO (YYYY-MM-DD) - opcional
    - end_date: Data final no formato ISO (YYYY-MM-DD) - opcional
    
    Retorna: Arquivo Excel com múltiplas abas (uma para cada tabela relacionada)
    """
    try:
        handler = get_data_handler()
        
        # Validar formato
        format = format.lower()
        if format not in ['xlsx', 'csv']:
            raise HTTPException(status_code=400, detail="Formato inválido. Use 'xlsx' ou 'csv'")
        
        # Mapear dashboard para tabelas relacionadas
        dashboard_tables = {
            'geral': ['financas'],
            'financas': ['financas'],
            'estoque': ['estoque'],
            'publico_alvo': ['publico_alvo'],
            'fornecedores': ['fornecedores'],
            'recursos_humanos': ['recursos_humanos']
        }
        
        dashboard_key = dashboard_name.lower()
        if dashboard_key not in dashboard_tables:
            raise HTTPException(status_code=404, detail=f"Dashboard '{dashboard_name}' não encontrado")
        
        tables = dashboard_tables[dashboard_key]
        
        # Carregar dados de todas as tabelas
        dataframes = {}
        for table in tables:
            table_key = table.lower().replace('_', '')
            
            if table_key in ['publicoalvo', 'fornecedores']:
                df = handler.load_full_unfiltered_table(table)
            else:
                if start_date and end_date:
                    handler.set_period(start_date, end_date)
                df = handler.load_table(table)
            
            if not df.empty:
                dataframes[table] = df
        
        if not dataframes:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para exportar")
        
        # Gerar nome do arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        date_suffix = ""
        if start_date and end_date:
            date_suffix = f"_{start_date}_{end_date}"
        filename = f"dashboard_{dashboard_name}{date_suffix}_{timestamp}.{format}"
        
        # Criar arquivo em memória
        output = io.BytesIO()
        
        if format == 'xlsx':
            # Exportar para Excel com múltiplas abas
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for table_name, df in dataframes.items():
                    # Limitar nome da aba (Excel tem limite de 31 caracteres)
                    sheet_name = table_name[:31]
                    df.to_excel(writer, index=False, sheet_name=sheet_name)
            
            output.seek(0)
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
        else:  # CSV - para múltiplas tabelas, criar um arquivo ZIP seria melhor, mas por simplicidade retornamos apenas a primeira
            # Para CSV, retornamos apenas a primeira tabela (ou poderia criar ZIP)
            first_table = list(dataframes.keys())[0]
            dataframes[first_table].to_csv(output, index=False, encoding='utf-8-sig')
            output.seek(0)
            media_type = "text/csv"
            filename = f"{first_table}{date_suffix}_{timestamp}.csv"
        
        # Retornar arquivo para download
        return StreamingResponse(
            io.BytesIO(output.read()),
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Banco de dados não encontrado: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar dados do dashboard: {str(e)}")

