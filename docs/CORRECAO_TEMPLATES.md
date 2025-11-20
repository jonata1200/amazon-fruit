# Correção - Templates HTML não sendo servidos

## Problema Identificado

Os templates HTML dos dashboards estavam retornando erro 404 porque:
1. O FastAPI não estava servindo a pasta `/templates`
2. O JavaScript estava buscando em `/static/templates/` em vez de `/templates/`

## Correções Aplicadas

### 1. Adicionar rota para servir templates no FastAPI

**Arquivo:** `backend/app/main.py`

```python
# Servir arquivos estáticos
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")
    # Servir templates HTML também
    app.mount("/templates", StaticFiles(directory=str(frontend_path / "templates")), name="templates")
```

### 2. Corrigir caminho no JavaScript

**Arquivo:** `frontend/static/js/app.js`

**Antes:**
```javascript
const response = await fetch(`/static/templates/dashboards/${dashboardName}.html`);
```

**Depois:**
```javascript
const response = await fetch(`/templates/dashboards/${dashboardName}.html`);
```

## Como Testar

1. Reinicie o servidor FastAPI:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. Acesse: http://localhost:8000

3. Navegue entre os dashboards:
   - Os templates HTML devem carregar corretamente
   - Os gráficos devem aparecer
   - As tabelas devem ser preenchidas

## Verificação

Após as correções, você não deve mais ver erros 404 para:
- `/templates/dashboards/geral.html`
- `/templates/dashboards/financas.html`
- `/templates/dashboards/estoque.html`
- `/templates/dashboards/publico_alvo.html`
- `/templates/dashboards/fornecedores.html`
- `/templates/dashboards/recursos_humanos.html`

