# Guia de Execução - Amazon Fruit

Este documento descreve como executar a aplicação Amazon Fruit pelo terminal.

## 📋 Pré-requisitos

Antes de executar, certifique-se de que:

1. ✅ **Python 3.11+** está instalado
2. ✅ **Ambiente virtual** está criado e ativado
3. ✅ **Dependências** estão instaladas (`pip install -r backend/requirements.txt`)
4. ✅ **Banco de dados** está criado (`data/amazon_fruit.db`)

> 💡 Se ainda não fez a instalação, consulte o arquivo [INSTALL.md](./INSTALL.md)

## 🚀 Executar a Aplicação

### Método 1: Execução Padrão (Recomendado)

**Windows (PowerShell):**
```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Linux/Mac:**
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**A partir da raiz do projeto:**
```bash
# Windows
cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Linux/Mac
cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Método 2: Execução com Variáveis de Ambiente

Você pode definir variáveis de ambiente antes de executar:

**Windows (PowerShell):**
```powershell
$env:ENVIRONMENT="development"
$env:DEBUG="True"
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Linux/Mac:**
```bash
export ENVIRONMENT=development
export DEBUG=True
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Método 3: Execução em Background (Windows)

Para executar em background no PowerShell:

```powershell
cd backend
Start-Process python -ArgumentList "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload" -WindowStyle Hidden
```

### Método 4: Execução em Background (Linux/Mac)

Para executar em background no Linux/Mac:

```bash
cd backend
nohup python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload > server.log 2>&1 &
```

Para ver os logs:
```bash
tail -f server.log
```

Para parar o servidor:
```bash
pkill -f "uvicorn app.main:app"
```

## 📍 Acessar a Aplicação

Após iniciar o servidor, a aplicação estará disponível em:

- **Frontend (Interface Principal):** http://localhost:8000
- **API REST:** http://localhost:8000/api
- **Documentação Swagger:** http://localhost:8000/docs
- **Documentação ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/api/health

## ⚙️ Opções de Execução

### Parâmetros do Uvicorn

| Parâmetro | Descrição | Padrão |
|-----------|-----------|--------|
| `--host` | Endereço IP para escutar | `127.0.0.1` (localhost) |
| `--port` | Porta do servidor | `8000` |
| `--reload` | Recarrega automaticamente ao detectar mudanças | Desabilitado |
| `--workers` | Número de processos worker | `1` |

### Exemplos de Uso

**Executar em todas as interfaces de rede:**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Executar em porta diferente:**
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8080
```

**Executar sem auto-reload (produção):**
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Executar com múltiplos workers (produção):**
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
```

## 🛑 Parar o Servidor

Para parar o servidor:

1. **No terminal onde está rodando:** Pressione `Ctrl + C`
2. **Se estiver em background:** Use o comando apropriado para seu sistema:
   - **Windows:** `Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process`
   - **Linux/Mac:** `pkill -f "uvicorn app.main:app"`

## 🔍 Verificar se o Servidor Está Rodando

**Windows (PowerShell):**
```powershell
netstat -ano | findstr :8000
```

**Linux/Mac:**
```bash
lsof -i :8000
# ou
netstat -tuln | grep 8000
```

## 🐛 Solução de Problemas

### Porta 8000 já está em uso

Se a porta 8000 estiver ocupada, você pode:

1. **Usar outra porta:**
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8080
   ```

2. **Encontrar e parar o processo que está usando a porta:**

   **Windows:**
   ```powershell
   # Encontrar processo
   netstat -ano | findstr :8000
   # Parar processo (substitua PID pelo número do processo)
   taskkill /PID <PID> /F
   ```

   **Linux/Mac:**
   ```bash
   # Encontrar processo
   lsof -i :8000
   # Parar processo (substitua PID pelo número do processo)
   kill -9 <PID>
   ```

### Erro de módulo não encontrado

Certifique-se de que:
1. O ambiente virtual está ativado
2. Você está no diretório `backend/` ou ajustou o PYTHONPATH
3. Todas as dependências estão instaladas: `pip install -r backend/requirements.txt`

### Erro de banco de dados não encontrado

Se aparecer erro sobre banco de dados:

1. **Gerar banco de dados de teste:**
   ```bash
   python scripts/generate_test_data.py data/amazon_fruit.db
   ```

2. **Verificar se o arquivo existe:**
   ```bash
   # Windows
   Test-Path data/amazon_fruit.db
   
   # Linux/Mac
   ls -la data/amazon_fruit.db
   ```

## 📝 Logs e Debugging

### Ver logs do servidor

Os logs aparecem diretamente no terminal onde o servidor está rodando.

### Modo Debug

Para ativar o modo debug, defina a variável de ambiente:

**Windows:**
```powershell
$env:DEBUG="True"
```

**Linux/Mac:**
```bash
export DEBUG=True
```

### Logs em arquivo

Para salvar logs em arquivo:

**Windows:**
```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload 2>&1 | Tee-Object -FilePath server.log
```

**Linux/Mac:**
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload 2>&1 | tee server.log
```

## 🎯 Comandos Rápidos

### Iniciar servidor (desenvolvimento)
```bash
cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Verificar saúde da API
```bash
curl http://localhost:8000/api/health
```

### Testar endpoint de dados
```bash
curl http://localhost:8000/api/data/date-range
```

## 📚 Próximos Passos

- Consulte [INSTALL.md](./INSTALL.md) para instruções de instalação
- Consulte [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) para resolver problemas comuns
- Consulte [DEPLOY.md](./DEPLOY.md) para instruções de deploy em produção

