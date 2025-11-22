# Guia de Teste Automatizado - Amazon Fruit Web App

## 📋 Descrição

Este guia explica como usar o script de teste automatizado (`test_web_app.py`) para verificar se todos os componentes da aplicação web estão funcionando corretamente.

## 🚀 Como Usar

### Passo 1: Certifique-se de que o servidor está rodando

Antes de executar os testes, você precisa ter o servidor FastAPI rodando:

```bash
# Ativar ambiente virtual
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac

# Iniciar servidor
cd backend
uvicorn app.main:app --reload --host localhost --port 8000
```

**⚠️ IMPORTANTE:** Mantenha o servidor rodando em um terminal separado!

### Passo 2: Executar o script de teste

Em outro terminal (com o ambiente virtual ativado):

```bash
# Na raiz do projeto
python test_web_app.py
```

## 📊 O que o Script Testa

O script executa **9 testes principais**:

### 1. Conexão com o Servidor
- Verifica se o servidor está respondendo
- Testa o endpoint `/api/health`

### 2. Estrutura de Arquivos
- Verifica se os arquivos principais existem:
  - `backend/app/main.py`
  - `frontend/templates/base.html`
  - `frontend/static/css/main.css`
  - `frontend/static/js/app.js`
  - Templates dos dashboards

### 3. Endpoint Raiz
- Testa se a página inicial (`/`) está sendo servida corretamente

### 4. Arquivos Estáticos
- Verifica se CSS e JavaScript estão sendo servidos:
  - `/static/css/main.css`
  - `/static/js/app.js`

### 5. Templates HTML
- Testa se todos os templates dos dashboards estão acessíveis:
  - `geral.html`
  - `financas.html`
  - `estoque.html`
  - `publico_alvo.html`
  - `fornecedores.html`
  - `recursos_humanos.html`

### 6. Endpoints de Dados
- Testa endpoints básicos de dados:
  - `/api/data/date-range`
  - `/api/test/data-handler`

### 7. Endpoints de Dashboard
- Testa todos os endpoints de dashboard:
  - `/api/dashboard/geral`
  - `/api/dashboard/financas`
  - `/api/dashboard/estoque`
  - `/api/dashboard/publico_alvo`
  - `/api/dashboard/fornecedores`
  - `/api/dashboard/recursos_humanos`

### 8. Endpoints de Análise
- Testa alguns endpoints de análise (amostra):
  - `/api/analysis/financial/summary`
  - `/api/analysis/inventory/summary`
  - `/api/analysis/suppliers/summary`

### 9. Endpoints de Gráficos
- Testa alguns endpoints de gráficos (amostra):
  - `/api/charts/financial/revenue-trend`
  - `/api/charts/inventory/stock-level`

## 📈 Interpretando os Resultados

### Saída do Script

O script mostra:
- **Cabeçalhos** para cada teste
- **Status de cada verificação**:
  - `[OK]` - Teste passou
  - `[ERRO]` - Teste falhou
  - `[AVISO]` - Algo pode estar errado, mas não crítico
  - `[INFO]` - Informações adicionais

### Relatório Final

No final, o script mostra:
- Total de testes executados
- Quantos passaram
- Quantos falharam
- Taxa de sucesso (%)
- Detalhes de cada teste

### Exemplo de Saída Bem-Sucedida

```
============================================================
                    RELATÓRIO FINAL
============================================================

Resumo dos Testes:
  Total de testes: 9
  [OK] Passou: 9
  [ERRO] Falhou: 0
  Taxa de sucesso: 100.0%

Detalhes:
  1. Conexão com Servidor: [PASSOU]
  2. Estrutura de Arquivos: [PASSOU]
  3. Endpoint Raiz: [PASSOU]
  4. Arquivos Estáticos: [PASSOU]
  5. Templates HTML: [PASSOU]
  6. Endpoints de Dados: [PASSOU]
  7. Endpoints de Dashboard: [PASSOU]
  8. Endpoints de Análise: [PASSOU]
  9. Endpoints de Gráficos: [PASSOU]

[SUCESSO] Todos os testes passaram!
```

## 🔧 Solução de Problemas

### Erro: "Não foi possível conectar ao servidor"

**Causa:** O servidor FastAPI não está rodando.

**Solução:**
1. Abra um terminal
2. Ative o ambiente virtual
3. Navegue para `backend/`
4. Execute: `uvicorn app.main:app --reload --host localhost --port 8000`
5. Mantenha esse terminal aberto
6. Execute o script de teste em outro terminal

### Erro: "ModuleNotFoundError: No module named 'requests'"

**Causa:** A biblioteca `requests` não está instalada.

**Solução:**
```bash
# Com ambiente virtual ativado
pip install requests
```

Ou instale todas as dependências:
```bash
pip install -r backend/requirements.txt
```

### Erro: Templates retornando 404

**Causa:** Os templates não estão sendo servidos corretamente.

**Solução:**
1. Verifique se `backend/app/main.py` tem a linha:
   ```python
   app.mount("/templates", StaticFiles(directory=str(frontend_path / "templates")), name="templates")
   ```
2. Reinicie o servidor FastAPI

### Erro: Arquivos estáticos não encontrados

**Causa:** Os arquivos estáticos não estão sendo servidos.

**Solução:**
1. Verifique se `backend/app/main.py` tem:
   ```python
   app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")
   ```
2. Verifique se os arquivos existem em `frontend/static/`
3. Reinicie o servidor

## 💡 Dicas

1. **Execute os testes regularmente** após fazer mudanças no código
2. **Mantenha o servidor rodando** em um terminal separado durante os testes
3. **Leia as mensagens de erro** - elas indicam exatamente o que está errado
4. **Use o script antes de fazer commit** para garantir que tudo está funcionando

## 📝 Personalização

Você pode modificar o script `test_web_app.py` para:
- Adicionar mais testes
- Mudar a URL base (variável `BASE_URL`)
- Ajustar o timeout (variável `TIMEOUT`)
- Adicionar testes específicos para suas necessidades

## 🎯 Próximos Passos

Após todos os testes passarem:
1. ✅ Aplicação está funcionando corretamente
2. ➡️ Continue com o desenvolvimento
3. ➡️ Execute testes antes de fazer deploy

