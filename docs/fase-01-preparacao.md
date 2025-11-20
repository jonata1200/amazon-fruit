# Fase 1: Preparação e Arquitetura Base

## Objetivo

Estabelecer a base técnica e arquitetural para a migração, garantindo que todos os componentes estejam mapeados e a estrutura web esteja definida.

## Duração Estimada

**1-2 semanas**

## Tarefas Detalhadas

### 1.1 Análise Completa do Código Existente

#### 1.1.1 Mapeamento de Dependências
- [ ] Listar todas as dependências do `requirements.txt`
- [ ] Identificar dependências específicas do PyQt6 que precisam ser substituídas
- [ ] Mapear bibliotecas que podem ser reutilizadas (pandas, numpy, etc.)
- [ ] Documentar versões atuais e compatibilidades

**Arquivos a analisar:**
- `requirements.txt`
- Todos os arquivos `.py` do projeto

#### 1.1.2 Mapeamento de Componentes UI
- [ ] Listar todos os widgets PyQt6 utilizados
- [ ] Mapear equivalentes web para cada widget:
  - `QPushButton` → `<button>` HTML + CSS/JS
  - `QLabel` → `<span>` ou `<div>` HTML
  - `QTableWidget` → `<table>` HTML ou componente de tabela JavaScript
  - `QStackedWidget` → Sistema de rotas ou tabs JavaScript
  - `QDateEdit` → `<input type="date">` HTML
  - `QProgressDialog` → Indicador de loading HTML/CSS
- [ ] Documentar padrões de estilo CSS utilizados

**Arquivos a analisar:**
- `modules/main_window.py`
- `modules/ui/widgets/*.py`
- `modules/app_styles.py`

#### 1.1.3 Mapeamento de Funcionalidades
- [ ] Listar todos os dashboards e suas funcionalidades
- [ ] Mapear métodos de análise e cálculos
- [ ] Identificar fluxos de dados entre componentes
- [ ] Documentar dependências entre módulos

**Checklist de funcionalidades:**
- [ ] Dashboard Geral - Evolução mensal, geração de relatório
- [ ] Dashboard Estoque - Tabelas, gráficos de produtos, rupturas
- [ ] Dashboard Finanças - KPIs, gráficos de receita/despesa
- [ ] Dashboard Público-Alvo - Gráficos de localização, gênero, canal
- [ ] Dashboard Fornecedores - Rankings, distribuição geográfica, matriz
- [ ] Dashboard Recursos Humanos - Headcount, custos, contratações
- [ ] Dashboard Insights - Análises avançadas
- [ ] Sistema de filtro de período
- [ ] Geração de relatórios PDF

### 1.2 Definição da Arquitetura Web

#### 1.2.1 Escolha do Framework Backend

**Opções:**
- **FastAPI** (Recomendado)
  - Vantagens: Performance, documentação automática, tipagem, async
  - Desvantagens: Curva de aprendizado se não conhecer
  
- **Flask**
  - Vantagens: Simples, flexível, grande comunidade
  - Desvantagens: Menos performático, sem tipagem nativa

**Decisão:** FastAPI (recomendado para APIs modernas)

#### 1.2.2 Estrutura de Pastas Proposta

```
amazon-fruit-web/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Aplicação FastAPI principal
│   │   ├── config.py             # Configurações
│   │   ├── database.py           # Conexão com SQLite
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── dashboard.py  # Rotas dos dashboards
│   │   │   │   ├── data.py       # Rotas de dados
│   │   │   │   ├── analysis.py   # Rotas de análises
│   │   │   │   └── reports.py    # Rotas de relatórios
│   │   ├── models/               # Modelos SQLAlchemy (se necessário)
│   │   ├── services/
│   │   │   ├── data_handler.py   # Migração do DataHandler
│   │   │   ├── analysis/         # Módulos de análise (reutilizar)
│   │   │   └── charts/           # Geração de gráficos Plotly
│   │   └── utils/                # Utilitários
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css
│   │   ├── js/
│   │   │   ├── app.js
│   │   │   ├── dashboards/
│   │   │   └── charts.js
│   │   └── images/
│   │       └── logo.png
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── dashboards/
│   │       ├── geral.html
│   │       ├── estoque.html
│   │       ├── financas.html
│   │       ├── publico_alvo.html
│   │       ├── fornecedores.html
│   │       ├── recursos_humanos.html
│   │       └── insights.html
│   └── package.json (se usar build tools)
├── data/                         # Manter estrutura atual
│   └── amazon_fruit.db
├── docs/                         # Documentação
├── tests/                        # Testes
├── docker-compose.yml (opcional)
├── Dockerfile (opcional)
└── README.md
```

#### 1.2.3 Arquitetura de Comunicação

```
Frontend (Browser)
    ↓ HTTP/HTTPS
Backend API (FastAPI)
    ↓ SQLAlchemy/Pandas
SQLite Database
```

**Fluxo de dados:**
1. Usuário interage com interface web
2. JavaScript faz requisição AJAX/Fetch para API
3. FastAPI processa requisição, acessa dados via DataHandler
4. Dados são processados (análises, cálculos)
5. Resposta JSON é enviada ao frontend
6. Frontend renderiza gráficos e tabelas

### 1.3 Setup do Ambiente de Desenvolvimento

#### 1.3.1 Criação do Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate
```

#### 1.3.2 Instalação de Dependências Base

**Novo `requirements.txt` (backend):**
```txt
# Framework Web
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Banco de Dados
sqlalchemy==2.0.23
aiosqlite==0.19.0  # Para async SQLite

# Análise de Dados (manter)
pandas==2.3.3
numpy==2.3.4

# Gráficos Web
plotly==5.18.0
kaleido==0.2.1  # Para exportar gráficos Plotly

# Relatórios (manter)
reportlab==4.4.4

# Utilitários
python-dateutil==2.9.0.post0
pytz==2025.2

# Desenvolvimento
pytest==7.4.3
pytest-asyncio==0.21.1
```

#### 1.3.3 Estrutura Inicial do Projeto

- [ ] Criar estrutura de pastas conforme definido
- [ ] Criar arquivo `backend/app/main.py` básico
- [ ] Criar arquivo `backend/requirements.txt`
- [ ] Configurar `.gitignore` adequado
- [ ] Criar arquivo de configuração `.env.example`

#### 1.3.4 Arquivo Base FastAPI

**`backend/app/main.py` (inicial):**
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(
    title="Amazon Fruit API",
    description="API para sistema de análise de dados Amazon Fruit",
    version="1.0.0"
)

# Servir arquivos estáticos
frontend_path = Path(__file__).parent.parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")

@app.get("/")
async def read_root():
    return FileResponse(str(frontend_path / "templates" / "index.html"))
```

### 1.4 Migração do DataHandler

#### 1.4.1 Análise do DataHandler Atual
- [ ] Revisar `modules/utils/data_handler.py`
- [ ] Identificar métodos que precisam ser adaptados
- [ ] Planejar conversão para async (opcional, mas recomendado)

#### 1.4.2 Estrutura do Novo DataHandler

**`backend/app/services/data_handler.py` (planejado):**
- Manter mesma interface pública
- Adaptar para trabalhar com SQLAlchemy (opcional)
- Manter compatibilidade com pandas
- Adicionar métodos async se necessário

### 1.5 Plano de Testes

#### 1.5.1 Estratégia de Testes
- [ ] Testes unitários para módulos de análise
- [ ] Testes de integração para API
- [ ] Testes de interface (opcional, com Selenium ou Playwright)

#### 1.5.2 Setup de Testes
- [ ] Configurar pytest
- [ ] Criar fixtures para banco de dados de teste
- [ ] Criar dados mock para testes

### 1.6 Documentação Inicial

- [ ] Documentar decisões arquiteturais
- [ ] Criar diagramas de arquitetura
- [ ] Documentar padrões de código a seguir
- [ ] Criar guia de contribuição

## Entregas da Fase 1

- [x] Documentação completa da análise do código existente
- [ ] Estrutura de pastas criada
- [ ] Ambiente de desenvolvimento configurado
- [ ] Aplicação FastAPI básica funcionando
- [ ] DataHandler migrado e testado
- [ ] Plano de testes definido

## Critérios de Aceitação

1. ✅ Ambiente de desenvolvimento funcionando
2. ✅ Aplicação FastAPI respondendo na porta 8000
3. ✅ Estrutura de pastas criada conforme especificado
4. ✅ DataHandler migrado e testado com dados reais
5. ✅ Documentação completa da arquitetura

## Próxima Fase

Após completar a Fase 1, seguir para **[Fase 2: API Backend](fase-02-api-backend.md)**

