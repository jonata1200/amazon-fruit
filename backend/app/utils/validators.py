# backend/app/utils/validators.py

"""
Validações customizadas para a aplicação
"""

from datetime import datetime
from typing import Optional
from fastapi import HTTPException

def validate_date(date_string: str, param_name: str = "date") -> str:
    """
    Valida uma string de data no formato YYYY-MM-DD.
    
    Args:
        date_string: String da data a validar
        param_name: Nome do parâmetro para mensagens de erro
    
    Returns:
        String da data validada
    
    Raises:
        HTTPException: Se a data for inválida
    """
    if not date_string:
        raise HTTPException(
            status_code=422,
            detail=f"{param_name} não pode ser vazio"
        )
    
    try:
        # Tentar fazer parse da data
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        
        # Verificar se a data é válida (datetime.strptime já valida mês/dia)
        # Mas vamos garantir que não há valores inválidos
        if date_obj.year < 1900 or date_obj.year > 2100:
            raise HTTPException(
                status_code=422,
                detail=f"{param_name} deve estar entre 1900 e 2100"
            )
        
        return date_string
        
    except ValueError as e:
        # Se o formato estiver errado ou valores inválidos (ex: 2020-13-01)
        raise HTTPException(
            status_code=422,
            detail=f"{param_name} inválida: '{date_string}'. Use o formato YYYY-MM-DD com valores válidos (ex: 2020-01-15)"
        )

def validate_date_range(start_date: str, end_date: str) -> tuple[str, str]:
    """
    Valida um intervalo de datas.
    
    Args:
        start_date: Data inicial
        end_date: Data final
    
    Returns:
        Tupla com (start_date, end_date) validadas
    
    Raises:
        HTTPException: Se as datas forem inválidas ou intervalo inválido
    """
    start = validate_date(start_date, "start_date")
    end = validate_date(end_date, "end_date")
    
    # Converter para datetime para comparar
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    
    if start_dt > end_dt:
        raise HTTPException(
            status_code=422,
            detail="start_date deve ser anterior ou igual a end_date"
        )
    
    # Verificar se o intervalo não é muito grande (opcional)
    days_diff = (end_dt - start_dt).days
    if days_diff > 3650:  # 10 anos
        raise HTTPException(
            status_code=422,
            detail="Intervalo de datas muito grande (máximo 10 anos)"
        )
    
    return start, end

def validate_query_string(query: str, min_length: int = 2, max_length: int = 100) -> str:
    """
    Valida uma string de busca.
    
    Args:
        query: String de busca
        min_length: Tamanho mínimo
        max_length: Tamanho máximo
    
    Returns:
        String validada e sanitizada
    
    Raises:
        HTTPException: Se a query for inválida
    """
    if not query:
        raise HTTPException(
            status_code=422,
            detail="Query de busca não pode ser vazia"
        )
    
    query = query.strip()
    
    if len(query) < min_length:
        raise HTTPException(
            status_code=422,
            detail=f"Query de busca deve ter pelo menos {min_length} caracteres"
        )
    
    if len(query) > max_length:
        raise HTTPException(
            status_code=422,
            detail=f"Query de busca deve ter no máximo {max_length} caracteres"
        )
    
    # Remover caracteres potencialmente perigosos (opcional)
    # query = query.replace("<", "").replace(">", "").replace("&", "")
    
    return query

