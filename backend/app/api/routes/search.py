# backend/app/api/routes/search.py

from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from typing import Optional, List, Dict
import pandas as pd

# Importar DataHandler
from ...services.data_handler import DataHandler
from ...utils.validators import validate_query_string

router = APIRouter(prefix="/api/search", tags=["search"])

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
async def global_search(
    q: str = Query(..., description="Termo de busca", min_length=2),
    limit: int = Query(10, description="Número máximo de resultados por categoria", ge=1, le=50)
):
    # Validar query de busca
    q = validate_query_string(q, min_length=2, max_length=100)
    """
    Busca global em todas as tabelas do sistema.
    
    Busca em:
    - Produtos (estoque)
    - Fornecedores
    - Clientes (público-alvo)
    - Funcionários (RH)
    - Categorias financeiras
    """
    try:
        if not q or len(q) < 2:
            raise HTTPException(status_code=400, detail="Termo de busca deve ter pelo menos 2 caracteres")
        
        handler = get_data_handler()
        query = q.lower().strip()
        results = {
            "query": q,
            "products": [],
            "suppliers": [],
            "customers": [],
            "employees": [],
            "financial": []
        }
        
        # 1. Buscar em produtos (estoque)
        try:
            df_estoque = handler.load_full_unfiltered_table('estoque')
            if not df_estoque.empty:
                # Buscar por nome do produto
                mask = df_estoque['Produto'].astype(str).str.lower().str.contains(query, na=False)
                produtos = df_estoque[mask].head(limit).to_dict(orient='records')
                results['products'] = [{
                    'id': p.get('Produto', ''),
                    'name': p.get('Produto', ''),
                    'stock': p.get('Quantidade_Estoque', 0),
                    'price': p.get('Preco_Venda', 0),
                    'type': 'product'
                } for p in produtos]
        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")
        
        # 2. Buscar em fornecedores
        try:
            df_fornecedores = handler.load_full_unfiltered_table('fornecedores')
            if not df_fornecedores.empty:
                mask = (
                    df_fornecedores['Nome_Fornecedor'].astype(str).str.lower().str.contains(query, na=False) |
                    df_fornecedores['Cidade'].astype(str).str.lower().str.contains(query, na=False) |
                    df_fornecedores['Estado'].astype(str).str.lower().str.contains(query, na=False)
                )
                fornecedores = df_fornecedores[mask].head(limit).to_dict(orient='records')
                results['suppliers'] = [{
                    'id': f.get('ID_Fornecedor', ''),
                    'name': f.get('Nome_Fornecedor', ''),
                    'city': f.get('Cidade', ''),
                    'state': f.get('Estado', ''),
                    'rating': f.get('Avaliacao', 0),
                    'type': 'supplier'
                } for f in fornecedores]
        except Exception as e:
            print(f"Erro ao buscar fornecedores: {e}")
        
        # 3. Buscar em clientes (público-alvo)
        try:
            df_publico = handler.load_full_unfiltered_table('publico_alvo')
            if not df_publico.empty:
                mask = (
                    df_publico['Cidade'].astype(str).str.lower().str.contains(query, na=False) |
                    df_publico['Canal_Venda'].astype(str).str.lower().str.contains(query, na=False)
                )
                clientes = df_publico[mask].head(limit).to_dict(orient='records')
                results['customers'] = [{
                    'id': c.get('ID_Cliente', ''),
                    'city': c.get('Cidade', ''),
                    'channel': c.get('Canal_Venda', ''),
                    'gender': c.get('Genero', ''),
                    'avg_spending': c.get('Gasto_Medio', 0),
                    'type': 'customer'
                } for c in clientes]
        except Exception as e:
            print(f"Erro ao buscar clientes: {e}")
        
        # 4. Buscar em funcionários (RH)
        try:
            df_rh = handler.load_full_unfiltered_table('recursos_humanos')
            if not df_rh.empty:
                mask = (
                    df_rh['Nome'].astype(str).str.lower().str.contains(query, na=False) |
                    df_rh['Cargo'].astype(str).str.lower().str.contains(query, na=False) |
                    df_rh['Departamento'].astype(str).str.lower().str.contains(query, na=False)
                )
                funcionarios = df_rh[mask].head(limit).to_dict(orient='records')
                results['employees'] = [{
                    'id': e.get('ID_Funcionario', ''),
                    'name': e.get('Nome', ''),
                    'role': e.get('Cargo', ''),
                    'department': e.get('Departamento', ''),
                    'salary': e.get('Salario', 0),
                    'type': 'employee'
                } for e in funcionarios]
        except Exception as e:
            print(f"Erro ao buscar funcionários: {e}")
        
        # 5. Buscar em categorias financeiras
        try:
            df_financas = handler.load_full_unfiltered_table('financas')
            if not df_financas.empty:
                mask = df_financas['Categoria'].astype(str).str.lower().str.contains(query, na=False)
                categorias = df_financas[mask]['Categoria'].unique()[:limit]
                results['financial'] = [{
                    'category': cat,
                    'type': 'financial_category'
                } for cat in categorias]
        except Exception as e:
            print(f"Erro ao buscar categorias financeiras: {e}")
        
        # Calcular total de resultados
        total = (
            len(results['products']) +
            len(results['suppliers']) +
            len(results['customers']) +
            len(results['employees']) +
            len(results['financial'])
        )
        
        return {
            "status": "success",
            "query": q,
            "total": total,
            "results": results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao realizar busca: {str(e)}")

