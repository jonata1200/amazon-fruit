# 🚀 Guia de Inicialização Rápida

## Iniciar o Servidor

### Windows (PowerShell) - Recomendado
```powershell
.\start-server.ps1
```

### Windows (CMD/Batch)
```cmd
start-server.bat
```

### Linux/Mac (Bash)
```bash
chmod +x start-server.sh
./start-server.sh
```

### Início Rápido (Windows PowerShell)
```powershell
.\start-server-quick.ps1
```

## 📋 O que os scripts fazem:

1. ✅ Verificam se Python está instalado
2. ✅ Verificam se as dependências estão instaladas
3. ✅ Verificam se a porta 8000 está livre
4. ✅ Iniciam o servidor FastAPI com reload automático

## 🌐 URLs Disponíveis:

- **Frontend:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/api/health

## ⚙️ Requisitos:

- Python 3.8+
- Dependências instaladas (`pip install -r backend/requirements.txt`)

## 🛑 Parar o Servidor:

Pressione `Ctrl+C` no terminal onde o servidor está rodando.

## 🔧 Troubleshooting:

### Porta 8000 já em uso:
```powershell
# Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force

# Linux/Mac
pkill -f "uvicorn app.main:app"
```

### Dependências não instaladas:
```bash
cd backend
pip install -r requirements.txt
```

### Erro de permissão (Linux/Mac):
```bash
chmod +x start-server.sh
```

