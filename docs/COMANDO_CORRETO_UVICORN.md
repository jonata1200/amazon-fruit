# ✅ Comando Correto para Executar o Uvicorn

## 🚨 Erro Comum

Você está executando:
```powershell
# ❌ ERRADO - Do diretório raiz
PS C:\Users\Jonata\Documents\GitHub\amazon-fruit> uvicorn app.main:app
```

## ✅ Solução Correta

### Passo a Passo

#### 1. Ativar Ambiente Virtual
```powershell
.venv\Scripts\Activate.ps1
```

Você deve ver `(.venv)` no prompt.

#### 2. Navegar para a Pasta Backend
```powershell
cd backend
```

**Verificação:** O prompt deve mostrar:
```
(.venv) PS C:\Users\Jonata\Documents\GitHub\amazon-fruit\backend>
```

#### 3. Executar o Uvicorn
```powershell
uvicorn app.main:app --reload --host localhost --port 8000
```

### 📋 Comandos Completos (Copy & Paste)

```powershell
# 1. Ativar ambiente virtual (se não estiver ativado)
.venv\Scripts\Activate.ps1

# 2. Ir para pasta backend
cd backend

# 3. Executar servidor
uvicorn app.main:app --reload --host localhost --port 8000
```

### 🎯 Resultado Esperado

Você deve ver:
```
INFO:     Will watch for changes in these directories: ['C:\\Users\\Jonata\\Documents\\GitHub\\amazon-fruit\\backend']
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 🌐 Acessar no Navegador

Com o servidor rodando, acesse:

- **Página inicial:** http://localhost:8000/
- **Health check:** http://localhost:8000/api/health
- **Swagger UI:** http://localhost:8000/docs

## 🔍 Por Que Precisa Estar na Pasta Backend?

O Python procura módulos relativos ao diretório atual:

```
Diretório Raiz (amazon-fruit/)
└─> Python procura: amazon-fruit/app/  ❌ Não existe

Diretório Backend (backend/)
└─> Python procura: backend/app/  ✅ Existe!
```

## ⚠️ Erros Comuns e Soluções

### Erro: "No module named 'app'"
**Causa:** Executando do diretório errado
**Solução:** `cd backend` antes de executar

### Erro: "No module named 'fastapi'"
**Causa:** Dependências não instaladas
**Solução:** `pip install -r requirements.txt`

### Erro: "Address already in use"
**Causa:** Porta 8000 já está em uso
**Solução:** Use outra porta: `--port 8001`

## 📝 Resumo Visual

```
┌─────────────────────────────────────────┐
│ 1. Ativar ambiente virtual             │
│    .venv\Scripts\Activate.ps1          │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 2. Ir para pasta backend               │
│    cd backend                           │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 3. Executar servidor                    │
│    uvicorn app.main:app --reload ...   │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 4. Acessar no navegador                │
│    http://localhost:8000/               │
└─────────────────────────────────────────┘
```

---

**Lembre-se:** Sempre execute o uvicorn a partir da pasta `backend/`!

