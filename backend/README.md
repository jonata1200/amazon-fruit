# Backend - Amazon Fruit API

## Configuração do Ambiente

### 1. Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e ajuste conforme necessário:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações.

### 4. Executar a Aplicação

```bash
# A partir do diretório backend/
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A aplicação estará disponível em:
- **API:** http://localhost:8000
- **Frontend:** http://localhost:8000/
- **Documentação Swagger:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health

## Estrutura do Projeto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicação FastAPI principal
│   ├── config.py             # Configurações
│   ├── api/
│   │   └── routes/           # Rotas da API
│   └── services/            # Lógica de negócio
│       ├── analysis/        # Módulos de análise
│       └── charts/          # Geração de gráficos
├── requirements.txt
└── README.md
```

## Próximos Passos

1. Migrar DataHandler para `app/services/data_handler.py`
2. Criar endpoints da API
3. Migrar módulos de análise
4. Implementar geração de gráficos Plotly

