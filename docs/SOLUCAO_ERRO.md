# 🔧 Solução para o Erro: ModuleNotFoundError

## Problema Identificado

O erro ocorre porque:
1. ❌ As dependências não foram instaladas
2. ⚠️ O ambiente virtual não está configurado corretamente

## ✅ Solução Passo a Passo

### Passo 1: Verificar/Criar Ambiente Virtual

**Opção A: Se o ambiente virtual NÃO existe**

```powershell
# No diretório raiz do projeto (amazon-fruit)
python -m venv .venv
```

**Opção B: Se o ambiente virtual JÁ existe**

Pule para o Passo 2.

### Passo 2: Ativar o Ambiente Virtual

```powershell
# No diretório raiz do projeto
.venv\Scripts\Activate.ps1
```

**Verificação:** Você deve ver `(.venv)` no início da linha do PowerShell.

**Se der erro de política de execução:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Passo 3: Verificar se o Python Correto Está Sendo Usado

```powershell
python -c "import sys; print(sys.executable)"
```

**Resultado esperado:** Deve mostrar algo como:
```
C:\Users\Jonata\Documents\GitHub\amazon-fruit\.venv\Scripts\python.exe
```

**Se mostrar o Python do sistema:** O ambiente virtual não está ativado corretamente. Volte ao Passo 2.

### Passo 4: Navegar para a Pasta Backend

```powershell
cd backend
```

### Passo 5: Instalar as Dependências

```powershell
pip install -r requirements.txt
```

**Tempo estimado:** 2-5 minutos

**O que será instalado:**
- fastapi
- uvicorn
- pandas
- numpy
- plotly
- E outras dependências...

### Passo 6: Verificar Instalação

```powershell
pip list | Select-String -Pattern "fastapi|uvicorn"
```

**Resultado esperado:**
```
fastapi    0.104.1
uvicorn    0.24.0
```

### Passo 7: Testar o Servidor

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Resultado esperado:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Passo 8: Testar no Navegador

Abra: http://localhost:8000/

---

## 🐛 Solução de Problemas Adicionais

### Problema: "pip não é reconhecido"

**Solução:**
```powershell
python -m pip install -r requirements.txt
```

### Problema: "Permission denied" ao criar venv

**Solução:** Execute o PowerShell como Administrador

### Problema: "Cannot activate virtual environment"

**Solução 1:** Verificar se o caminho está correto
```powershell
Test-Path .venv\Scripts\Activate.ps1
```

**Solução 2:** Usar caminho completo
```powershell
& "C:\Users\Jonata\Documents\GitHub\amazon-fruit\.venv\Scripts\Activate.ps1"
```

### Problema: Dependências não instalam

**Solução:** Atualizar pip primeiro
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## ✅ Checklist de Verificação

Após seguir os passos, verifique:

- [ ] Ambiente virtual criado (pasta `.venv` existe)
- [ ] Ambiente virtual ativado (`(.venv)` no prompt)
- [ ] Python correto em uso (caminho mostra `.venv`)
- [ ] Dependências instaladas (`pip list` mostra fastapi e uvicorn)
- [ ] Servidor inicia sem erros
- [ ] Página carrega no navegador

---

## 📝 Comandos Rápidos (Copy & Paste)

```powershell
# 1. Criar ambiente virtual (se necessário)
python -m venv .venv

# 2. Ativar ambiente virtual
.venv\Scripts\Activate.ps1

# 3. Ir para backend
cd backend

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Verificar instalação
pip list | Select-String -Pattern "fastapi|uvicorn"

# 6. Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🎯 Resultado Esperado

Após seguir todos os passos:

✅ Servidor rodando na porta 8000  
✅ Página inicial acessível em http://localhost:8000/  
✅ Health check funcionando em http://localhost:8000/api/health  
✅ Swagger UI disponível em http://localhost:8000/docs  

