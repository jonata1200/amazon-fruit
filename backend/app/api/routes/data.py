# backend/app/api/routes/data.py

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from pathlib import Path

# Importação relativa do DataHandler
from ...services.data_handler import DataHandler

router = APIRouter(prefix="/api/data", tags=["data"])

# Instância global do DataHandler (será inicializada no startup)
_data_handler: Optional[DataHandler] = None

def get_data_handler() -> DataHandler:
    """Obtém ou cria uma instância do DataHandler"""
    global _data_handler
    if _data_handler is None:
        # Calcula o diretório raiz do projeto
        # Este arquivo está em: backend/app/api/routes/data.py
        # Precisamos subir 4 níveis: routes -> api -> app -> backend -> raiz
        project_root = Path(__file__).resolve().parents[4]
        _data_handler = DataHandler(base_dir=project_root)
    return _data_handler

@router.get("/{table_name}")
async def get_table_data(
    table_name: str,
    start_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)")
):
    """
    Retorna dados de uma tabela específica.
    
    Parâmetros:
    - table_name: Nome da tabela (financas, estoque, publico_alvo, fornecedores, recursos_humanos)
    - start_date: Data inicial no formato ISO (YYYY-MM-DD) - opcional
    - end_date: Data final no formato ISO (YYYY-MM-DD) - opcional
    
    Retorna: JSON com os dados da tabela
    """
    try:
        handler = get_data_handler()
        
        # Se datas foram fornecidas, configura o período
        if start_date and end_date:
            handler.set_period(start_date, end_date)
        
        # Carrega os dados
        df = handler.load_table(table_name)
        
        # Converte DataFrame para JSON
        # Usa orient='records' para retornar lista de objetos
        return {
            "status": "success",
            "table_name": table_name,
            "count": len(df),
            "data": df.to_dict(orient='records')
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Banco de dados não encontrado: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dados: {str(e)}")

@router.get("/{table_name}/comparative")
async def get_comparative_data(
    table_name: str,
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")
):
    """
    Retorna dados comparativos (período atual vs período anterior).
    
    Parâmetros:
    - table_name: Nome da tabela
    - start_date: Data inicial do período atual (YYYY-MM-DD)
    - end_date: Data final do período atual (YYYY-MM-DD)
    
    Retorna: JSON com dados do período atual e anterior
    """
    try:
        handler = get_data_handler()
        handler.set_period(start_date, end_date)
        
        df_current, df_previous = handler.load_comparative_data(table_name)
        
        return {
            "status": "success",
            "table_name": table_name,
            "period": {
                "start": start_date,
                "end": end_date
            },
            "current": {
                "count": len(df_current),
                "data": df_current.to_dict(orient='records')
            },
            "previous": {
                "count": len(df_previous),
                "data": df_previous.to_dict(orient='records')
            }
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Banco de dados não encontrado: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dados comparativos: {str(e)}")

@router.get("/date-range")
async def get_date_range():
    """
    Retorna o range de datas disponível no banco de dados.
    
    Retorna: JSON com min_date e max_date
    """
    try:
        handler = get_data_handler()
        min_date, max_date = handler.get_date_range()
        
        if min_date is None or max_date is None:
            return {
                "status": "warning",
                "message": "Nenhuma data encontrada no banco de dados",
                "min_date": None,
                "max_date": None
            }
        
        return {
            "status": "success",
            "min_date": min_date.strftime('%Y-%m-%d'),
            "max_date": max_date.strftime('%Y-%m-%d')
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Banco de dados não encontrado: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter range de datas: {str(e)}")
