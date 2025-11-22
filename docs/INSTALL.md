# Guia de Instalação - Amazon Fruit

Este documento descreve como instalar e configurar a aplicação Amazon Fruit para desenvolvimento local.

## 📋 Pré-requisitos

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **SQLite3** (geralmente incluído com Python)

### Opcional

- **Docker** ([Download](https://www.docker.com/get-started)) - Para usar containerização
- **Node.js** - Não necessário (aplicação usa JavaScript vanilla)

## 🚀 Instalação Rápida

### 1. Clonar Repositório

```bash
git clone <url-do-repositorio>
cd amazon-fruit
```

### 2. Criar Ambiente Virtual

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### 4. Configurar Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas configurações (opcional)
# Os valores padrão funcionam para desenvolvimento local
```

### 5. Verificar Banco de Dados

```bash
# Verificar se o banco de dados existe
ls -la data/amazon_fruit.db

# Se não existir, você precisará importar os dados
# Consulte a documentação de migração de dados
```

### 6. Iniciar Aplicação

```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 7. Acessar Aplicação

Abra seu navegador em: `http://localhost:8000`

## 🐳 Instalação com Docker

### 1. Build da Imagem

```bash
docker build -t amazon-fruit .
```

### 2. Executar Container

```bash
docker run -d \
  --name amazon-fruit \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data:ro \
  amazon-fruit
```

### 3. Com Docker Compose

```bash
# Desenvolvimento
docker-compose up

# Produção
docker-compose -f docker-compose.yml up -d
```

## 🔧 Configuração Detalhada

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Ambiente
ENVIRONMENT=development
DEBUG=True

# Banco de Dados
DB_PATH=./data/amazon_fruit.db

# API
API_HOST=127.0.0.1
API_PORT=8000

# CORS
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### Estrutura de Diretórios

```
amazon-fruit/
├── backend/          # Código backend (FastAPI)
│   ├── app/
│   └── requirements.txt
├── frontend/        # Código frontend (HTML/CSS/JS)
│   ├── static/
│   └── templates/
├── data/            # Banco de dados e dados Excel
│   └── amazon_fruit.db
├── docs/            # Documentação
├── scripts/          # Scripts utilitários
└── .env             # Variáveis de ambiente
```

## 🧪 Verificar Instalação

### 1. Testar API

```bash
# Health check
curl http://localhost:8000/api/health

# Deve retornar:
{
  "status": "healthy",
  "message": "API está funcionando corretamente"
}
```

### 2. Testar DataHandler

```bash
curl http://localhost:8000/api/test/data-handler
```

### 3. Acessar Interface Web

Abra `http://localhost:8000` no navegador e verifique:
- ✅ Página carrega corretamente
- ✅ Sidebar aparece
- ✅ Dashboards carregam
- ✅ Gráficos renderizam

## 📦 Dependências Principais

- **FastAPI** - Framework web
- **Uvicorn** - Servidor ASGI
- **SQLAlchemy** - ORM
- **Pandas** - Análise de dados
- **Plotly** - Gráficos
- **OpenPyXL** - Exportação Excel

## 🐛 Problemas Comuns

### Erro: Módulo não encontrado

```bash
# Verificar se o ambiente virtual está ativo
which python  # Deve apontar para venv/bin/python

# Reinstalar dependências
pip install -r backend/requirements.txt
```

### Erro: Porta 8000 já em uso

```bash
# Verificar processo usando a porta
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Usar porta diferente
uvicorn app.main:app --port 8001
```

### Erro: Banco de dados não encontrado

```bash
# Verificar se o arquivo existe
ls -la data/amazon_fruit.db

# Se não existir, você precisa importar os dados
# Consulte scripts/migrate_excel_to_sqlite.py
```

### Erro: Permissão negada

```bash
# Linux/Mac: Dar permissão de execução aos scripts
chmod +x scripts/*.sh

# Verificar permissões do banco de dados
chmod 644 data/amazon_fruit.db
```

## 🚀 Scripts de Inicialização Rápida

### Windows

```powershell
# Usar script PowerShell
.\start-server-quick.ps1
```

### Linux/Mac

```bash
# Usar script Bash
chmod +x start-server.sh
./start-server.sh
```

## 📚 Próximos Passos

Após instalação bem-sucedida:

1. **Explorar Dashboards**
   - Acesse os diferentes dashboards disponíveis
   - Teste filtros e exportações

2. **Ler Documentação**
   - `docs/README.md` - Visão geral
   - `docs/DEPLOY.md` - Guia de deploy
   - `docs/TROUBLESHOOTING.md` - Solução de problemas

3. **Desenvolvimento**
   - Estrutura do código está em `backend/app/`
   - Frontend em `frontend/`

## 🔄 Atualização

```bash
# Pull das mudanças
git pull

# Atualizar dependências
pip install -r backend/requirements.txt --upgrade

# Reiniciar aplicação
```

## 📞 Suporte

Se encontrar problemas:

1. Verificar logs da aplicação
2. Consultar `docs/TROUBLESHOOTING.md`
3. Verificar issues no repositório
4. Criar nova issue se necessário

---

**Última atualização:** 2025-01-XX

