# Fase 2: API Backend

## Objetivo

Criar a API REST completa que servirá como backend da aplicação web, migrando toda a lógica de negócio e disponibilizando endpoints para o frontend consumir.

## Duração Estimada

**2-3 semanas**

## Tarefas Detalhadas

### 2.1 Migração Completa do DataHandler

#### 2.1.1 Criação do Novo DataHandler

**Arquivo:** `backend/app/services/data_handler.py`

**Objetivos:**
- Manter a mesma interface pública do DataHandler original
- Adaptar para trabalhar em ambiente web
- Manter compatibilidade com pandas
- Adicionar suporte a async (opcional, mas recomendado)

**Estrutura proposta:**
```python
from pathlib import Path
import sqlite3
import pandas as pd
from typing import Optional, Tuple

class DataHandler:
    def __init__(self, base_dir: Optional[Path] = None):
        # Mesma lógica do original
        pass
    
    def set_period(self, start_iso: str, end_iso: str):
        # Mesma implementação
        pass
    
    def load_table(self, name: str) -> pd.DataFrame:
        # Mesma implementação
        pass
    
    def load_comparative_data(self, name: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        # Mesma implementação
        pass
    
    def get_date_range(self) -> Tuple[pd.Timestamp, pd.Timestamp]:
        # Mesma implementação
        pass
```

**Tarefas:**
- [ ] Copiar código do `modules/utils/data_handler.py`
- [ ] Adaptar imports e caminhos
- [ ] Testar com dados reais
- [ ] Adicionar tratamento de erros melhorado
- [ ] Adicionar logging

#### 2.1.2 Testes do DataHandler

- [ ] Criar testes unitários para cada método
- [ ] Testar com diferentes períodos
- [ ] Testar com dados vazios
- [ ] Testar tratamento de erros

### 2.2 Criação dos Endpoints da API

#### 2.2.1 Estrutura de Rotas

**Arquivo:** `backend/app/api/routes/__init__.py`
- Organizar rotas por funcionalidade
- Usar routers do FastAPI

#### 2.2.2 Endpoints de Dados

**Arquivo:** `backend/app/api/routes/data.py`

**Endpoints necessários:**

```python
@router.get("/api/data/{table_name}")
async def get_table_data(
    table_name: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Retorna dados de uma tabela específica.
    
    Parâmetros:
    - table_name: Nome da tabela (financas, estoque, etc.)
    - start_date: Data inicial (ISO format: YYYY-MM-DD)
    - end_date: Data final (ISO format: YYYY-MM-DD)
    
    Retorna: JSON com os dados da tabela
    """
    pass

@router.get("/api/data/{table_name}/comparative")
async def get_comparative_data(
    table_name: str,
    start_date: str,
    end_date: str
):
    """
    Retorna dados comparativos (período atual vs anterior).
    
    Retorna: JSON com dados atuais e anteriores
    """
    pass

@router.get("/api/data/date-range")
async def get_date_range():
    """
    Retorna o range de datas disponível no banco.
    
    Retorna: JSON com min_date e max_date
    """
    pass
```

**Tarefas:**
- [ ] Implementar endpoint `/api/data/{table_name}`
- [ ] Implementar endpoint `/api/data/{table_name}/comparative`
- [ ] Implementar endpoint `/api/data/date-range`
- [ ] Adicionar validação de parâmetros
- [ ] Adicionar tratamento de erros
- [ ] Adicionar documentação Swagger automática
- [ ] Testar todos os endpoints

#### 2.2.3 Endpoints de Análises

**Arquivo:** `backend/app/api/routes/analysis.py`

**Reutilizar módulos existentes:**
- `modules/analysis/financial_analysis.py`
- `modules/analysis/inventory_analysis.py`
- `modules/analysis/suppliers_analysis.py`
- `modules/analysis/public_analysis.py`
- `modules/analysis/hr_analysis.py`

**Endpoints necessários:**

```python
@router.get("/api/analysis/financial/summary")
async def get_financial_summary(
    start_date: str,
    end_date: str
):
    """
    Retorna resumo financeiro (receita, despesa, lucro).
    
    Retorna: JSON com valores e variações percentuais
    """
    pass

@router.get("/api/analysis/financial/top-expenses")
async def get_top_expenses(
    start_date: str,
    end_date: str,
    top_n: int = 5
):
    """
    Retorna top N despesas por categoria.
    """
    pass

@router.get("/api/analysis/financial/top-revenues")
async def get_top_revenues(
    start_date: str,
    end_date: str,
    top_n: int = 5
):
    """
    Retorna top N receitas por categoria.
    """
    pass

@router.get("/api/analysis/inventory/top-selling")
async def get_top_selling_items(
    start_date: str,
    end_date: str,
    top_n: int = 10
):
    """
    Retorna top N produtos mais vendidos.
    """
    pass

@router.get("/api/analysis/inventory/low-stock")
async def get_low_stock_items(
    start_date: str,
    end_date: str,
    top_n: int = 10
):
    """
    Retorna produtos com estoque baixo.
    """
    pass

# ... mais endpoints para outras análises
```

**Tarefas:**
- [ ] Criar wrapper para cada função de análise
- [ ] Converter resultados pandas para JSON
- [ ] Implementar todos os endpoints de análise
- [ ] Adicionar cache (opcional, com Redis ou memória)
- [ ] Testar todos os endpoints

#### 2.2.4 Endpoints de Dashboards

**Arquivo:** `backend/app/api/routes/dashboard.py`

**Endpoints agregados:**

```python
@router.get("/api/dashboard/geral")
async def get_dashboard_geral(
    start_date: str,
    end_date: str
):
    """
    Retorna todos os dados necessários para o dashboard geral.
    
    Retorna: JSON com dados financeiros e gráficos
    """
    pass

@router.get("/api/dashboard/estoque")
async def get_dashboard_estoque(
    start_date: str,
    end_date: str
):
    """
    Retorna dados do dashboard de estoque.
    """
    pass

@router.get("/api/dashboard/financas")
async def get_dashboard_financas(
    start_date: str,
    end_date: str
):
    """
    Retorna dados do dashboard de finanças.
    """
    pass

# ... endpoints para outros dashboards
```

**Tarefas:**
- [ ] Criar endpoint para cada dashboard
- [ ] Agregar dados de múltiplas fontes
- [ ] Otimizar queries para reduzir tempo de resposta
- [ ] Testar performance

#### 2.2.5 Endpoints de Gráficos

**Arquivo:** `backend/app/api/routes/charts.py`

**Estratégia:**
- Opção 1: Gerar gráficos Plotly no backend e retornar JSON
- Opção 2: Retornar dados e gerar gráficos no frontend (recomendado)

**Endpoints:**

```python
@router.get("/api/charts/financial/evolution")
async def get_financial_evolution_chart(
    start_date: str,
    end_date: str
):
    """
    Retorna dados formatados para gráfico de evolução financeira.
    
    Retorna: JSON com estrutura Plotly
    """
    pass

@router.get("/api/charts/inventory/top-selling")
async def get_top_selling_chart(
    start_date: str,
    end_date: str
):
    """
    Retorna dados para gráfico de top produtos.
    """
    pass

# ... mais endpoints de gráficos
```

**Tarefas:**
- [ ] Migrar funções de `chart_generator.py` para Plotly
- [ ] Criar funções que retornam dados Plotly JSON
- [ ] Implementar todos os endpoints de gráficos
- [ ] Testar renderização no frontend

### 2.3 Migração dos Módulos de Análise

#### 2.3.1 Estrutura de Migração

**Estratégia:** Reutilizar código existente, apenas adaptar imports

**Arquivos a migrar:**
- `modules/analysis/financial_analysis.py` → `backend/app/services/analysis/financial_analysis.py`
- `modules/analysis/inventory_analysis.py` → `backend/app/services/analysis/inventory_analysis.py`
- `modules/analysis/suppliers_analysis.py` → `backend/app/services/analysis/suppliers_analysis.py`
- `modules/analysis/public_analysis.py` → `backend/app/services/analysis/public_analysis.py`
- `modules/analysis/hr_analysis.py` → `backend/app/services/analysis/hr_analysis.py`

**Tarefas:**
- [ ] Copiar arquivos para nova estrutura
- [ ] Ajustar imports
- [ ] Testar cada módulo isoladamente
- [ ] Adicionar type hints (opcional)
- [ ] Adicionar docstrings melhoradas

### 2.4 Migração do Sistema de Gráficos

#### 2.4.1 Conversão de Matplotlib para Plotly

**Arquivo:** `backend/app/services/charts/chart_generator.py`

**Estratégia:**
- Substituir matplotlib por Plotly
- Manter mesma lógica de dados
- Adaptar estilo visual

**Exemplo de conversão:**

**Antes (Matplotlib):**
```python
def create_finance_evolution_chart(df_fin: pd.DataFrame) -> Figure:
    fig, ax = plt.subplots()
    monthly[['Receita', 'Despesa']].plot(kind='bar', ax=ax)
    return fig
```

**Depois (Plotly):**
```python
import plotly.graph_objects as go
import plotly.express as px

def create_finance_evolution_chart(df_fin: pd.DataFrame) -> dict:
    # Preparar dados
    monthly = prepare_monthly_data(df_fin)
    
    # Criar gráfico Plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly.index, y=monthly['Receita'], name='Receita'))
    fig.add_trace(go.Bar(x=monthly.index, y=monthly['Despesa'], name='Despesa'))
    
    # Retornar como dict (JSON serializable)
    return fig.to_dict()
```

**Tarefas:**
- [ ] Converter `create_general_evolution_chart`
- [ ] Converter `create_finance_evolution_chart`
- [ ] Converter `create_top_expenses_chart`
- [ ] Converter `create_top_revenues_chart`
- [ ] Converter todos os gráficos de estoque
- [ ] Converter todos os gráficos de fornecedores
- [ ] Converter todos os gráficos de público-alvo
- [ ] Converter todos os gráficos de RH
- [ ] Manter paleta de cores similar
- [ ] Testar cada gráfico

### 2.5 Sistema de Relatórios PDF

#### 2.5.1 Endpoint de Geração de Relatórios

**Arquivo:** `backend/app/api/routes/reports.py`

**Estratégia:**
- Manter uso do reportlab
- Gerar PDF no backend
- Retornar como download

**Endpoint:**

```python
@router.get("/api/reports/full")
async def generate_full_report(
    start_date: str,
    end_date: str
):
    """
    Gera relatório completo em PDF.
    
    Retorna: Arquivo PDF para download
    """
    # Reutilizar ReportGenerator existente
    # Adaptar para trabalhar com FastAPI
    pass
```

**Tarefas:**
- [ ] Migrar `modules/report/report_generator.py`
- [ ] Adaptar para gerar PDF em memória
- [ ] Criar endpoint de download
- [ ] Testar geração de relatórios

### 2.6 Configuração e Middleware

#### 2.6.1 Configurações

**Arquivo:** `backend/app/config.py`

```python
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Caminho do banco de dados
    db_path: Path = Path("data/amazon_fruit.db")
    
    # Configurações da API
    api_title: str = "Amazon Fruit API"
    api_version: str = "1.0.0"
    
    # CORS
    cors_origins: list = ["http://localhost:8000", "http://127.0.0.1:8000"]
    
    class Config:
        env_file = ".env"
```

#### 2.6.2 Middleware

- [ ] Configurar CORS
- [ ] Adicionar logging de requisições
- [ ] Adicionar tratamento de erros global
- [ ] Adicionar rate limiting (opcional)

### 2.7 Documentação da API

#### 2.7.1 Swagger/OpenAPI

- [ ] FastAPI gera automaticamente documentação Swagger
- [ ] Acessar em `/docs` após implementação
- [ ] Adicionar descrições detalhadas nos endpoints
- [ ] Adicionar exemplos de requisições/respostas

#### 2.7.2 Documentação Manual

- [ ] Criar arquivo `docs/API.md` com documentação
- [ ] Listar todos os endpoints
- [ ] Exemplos de uso
- [ ] Códigos de erro possíveis

### 2.8 Testes da API

#### 2.8.1 Testes Unitários

**Arquivo:** `tests/test_api/`

- [ ] Testes para cada endpoint
- [ ] Testes com dados mock
- [ ] Testes de validação
- [ ] Testes de tratamento de erros

#### 2.8.2 Testes de Integração

- [ ] Testes end-to-end
- [ ] Testes com banco de dados real
- [ ] Testes de performance

## Entregas da Fase 2

- [ ] DataHandler migrado e funcionando
- [ ] Todos os endpoints de dados implementados
- [ ] Todos os endpoints de análise implementados
- [ ] Todos os endpoints de dashboards implementados
- [ ] Sistema de gráficos Plotly funcionando
- [ ] Sistema de relatórios PDF funcionando
- [ ] API documentada (Swagger)
- [ ] Testes implementados
- [ ] API respondendo corretamente a todas as requisições

## Critérios de Aceitação

1. ✅ Todos os endpoints retornam dados corretos
2. ✅ Gráficos Plotly são gerados corretamente
3. ✅ Relatórios PDF são gerados corretamente
4. ✅ API tem documentação Swagger completa
5. ✅ Testes passando com cobertura > 80%
6. ✅ Performance aceitável (< 2s para dashboards)

## Próxima Fase

Após completar a Fase 2, seguir para **[Fase 3: Migração dos Dashboards](fase-03-dashboards.md)**

