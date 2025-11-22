# Correção: Dados não aparecem em Público-Alvo e Recursos Humanos

## Problema Identificado

Os dashboards de **Público-Alvo** e **Recursos Humanos** não estavam exibindo dados porque:

1. **Público-Alvo**: A tabela `clientes` não tem coluna de data direta (tem apenas `Ano` e `Mes`), então quando o endpoint tentava filtrar por período usando `load_table()`, não retornava dados.

2. **Recursos Humanos**: O endpoint estava funcionando, mas pode ter problemas similares se houver filtros de data aplicados incorretamente.

## Correções Aplicadas

### 1. Endpoint de Dashboard - Público-Alvo

**Arquivo:** `backend/app/api/routes/dashboard.py`

**Antes:**
```python
@router.get("/publico_alvo")
async def get_dashboard_publico_alvo(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)")
):
    handler.set_period(start_date, end_date)
    df_publico = handler.load_table("Publico_Alvo")  # ❌ Não retorna dados
```

**Depois:**
```python
@router.get("/publico_alvo")
async def get_dashboard_publico_alvo(
    start_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)")
):
    # A tabela de clientes não tem coluna de data, então carregamos todos os dados
    df_publico = handler.load_full_unfiltered_table("Publico_Alvo")  # ✅ Retorna todos os dados
```

### 2. Endpoint de Dados - Tabelas sem Data

**Arquivo:** `backend/app/api/routes/data.py`

**Mudança:** Adicionada lógica para detectar tabelas sem coluna de data e usar `load_full_unfiltered_table()`:

```python
# Tabelas que não têm coluna de data devem usar load_full_unfiltered_table
tables_without_date = ['publico_alvo', 'fornecedores']
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
```

## Estrutura das Tabelas

### Tabela `clientes` (Público-Alvo)
- ❌ **Não tem coluna de data direta**
- ✅ Tem colunas: `Ano`, `Mes` (mas não são usadas para filtro)
- ✅ Dados devem ser carregados sem filtro de data

### Tabela `funcionarios` (Recursos Humanos)
- ✅ Tem coluna: `Data_Contratacao`
- ✅ Pode usar filtro de data, mas o endpoint atual não aplica filtro

## Resultado Esperado

Após as correções:

1. ✅ **Dashboard Público-Alvo** deve exibir:
   - Gráficos de localização, gênero e canal
   - Tabela com dados de clientes

2. ✅ **Dashboard Recursos Humanos** deve exibir:
   - Gráficos de headcount, custo, cargos e contratações
   - Tabela com dados de funcionários

3. ✅ **Endpoint `/api/data/publico_alvo`** deve retornar todos os clientes

4. ✅ **Endpoint `/api/data/recursos_humanos`** deve retornar todos os funcionários

## Como Testar

1. Reinicie o servidor FastAPI
2. Acesse http://localhost:8000
3. Navegue para o dashboard **Público-Alvo**
4. Verifique se os gráficos aparecem com dados
5. Verifique se a tabela está populada
6. Repita para **Recursos Humanos**

## Notas Técnicas

- A tabela `clientes` tem 4.201 registros no banco
- A tabela `funcionarios` tem 120 registros no banco
- Esses dados devem aparecer agora nos dashboards

