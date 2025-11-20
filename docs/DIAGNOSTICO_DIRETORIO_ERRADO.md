# 🔍 Diagnóstico: Erro de Diretório ao Executar Uvicorn

## 📊 Análise do Problema

### Erro Observado
```
ModuleNotFoundError: No module named 'app'
```

### 🔎 Diagnóstico Detalhado

#### 1. **Problema Identificado: Diretório de Execução Incorreto**

**Evidências:**
- ❌ Comando executado do diretório raiz: `C:\Users\Jonata\Documents\GitHub\amazon-fruit`
- ❌ Comando usado: `uvicorn app.main:app`
- ✅ Módulo `app` está em: `backend/app/`
- ❌ Python não encontra o módulo porque está no diretório errado

**Causa Raiz:**
O comando `uvicorn app.main:app` está sendo executado do diretório **raiz do projeto**, mas o módulo `app` está dentro da pasta `backend/`.

### 📋 Estrutura do Projeto

```
amazon-fruit/                    ← Você está AQUI
├── backend/
│   └── app/                     ← Módulo 'app' está AQUI
│       ├── __init__.py
│       ├── main.py
│       └── config.py
└── frontend/
```

### 🔍 Sequência de Eventos

```
1. Usuário executa comando do diretório raiz
   └─> PS C:\Users\Jonata\Documents\GitHub\amazon-fruit>
   └─> uvicorn app.main:app

2. Python tenta encontrar o módulo 'app'
   └─> Procura em: amazon-fruit/app/  ❌ Não existe
   └─> Deveria procurar em: amazon-fruit/backend/app/  ✅ Existe

3. Erro: ModuleNotFoundError
   └─> Python não encontra o módulo
```

### ✅ Verificações Realizadas

| Item | Status | Detalhes |
|------|--------|----------|
| Diretório atual | ❌ Raiz | `amazon-fruit/` |
| Diretório correto | ✅ backend/ | Deveria estar em `backend/` |
| Módulo app existe | ✅ SIM | `backend/app/main.py` existe |
| Comando correto | ⚠️ PARCIAL | Comando OK, mas diretório errado |

### 🎯 Causa Raiz Identificada

**PRINCIPAL:** Comando executado do diretório errado (raiz ao invés de `backend/`)

**SOLUÇÃO:** Executar o comando a partir da pasta `backend/`

### 🔧 Soluções Possíveis

#### Solução 1: Navegar para pasta backend (Recomendado)

```powershell
# 1. Navegar para a pasta backend
cd backend

# 2. Executar o comando
uvicorn app.main:app --reload --host localhost --port 8000
```

#### Solução 2: Usar caminho completo (Alternativa)

```powershell
# Do diretório raiz, usar caminho completo
uvicorn backend.app.main:app --reload --host localhost --port 8000
```

**Nota:** Solução 1 é mais simples e recomendada.

### 📝 Comandos Corretos

#### Opção A: Comando Completo (Recomendado)
```powershell
cd backend
uvicorn app.main:app --reload --host localhost --port 8000
```

#### Opção B: Em uma linha
```powershell
cd backend; uvicorn app.main:app --reload --host localhost --port 8000
```

### ✅ Checklist de Verificação

Antes de executar, verifique:

- [ ] Está na pasta `backend/`? (`cd backend`)
- [ ] Arquivo `app/main.py` existe? (`Test-Path app\main.py`)
- [ ] Ambiente virtual está ativado? (`(.venv)` no prompt)
- [ ] Dependências instaladas? (`pip list | Select-String fastapi`)

### 🎯 Resumo

| Item | Status Atual | Status Correto |
|------|-------------|----------------|
| Diretório | ❌ Raiz (`amazon-fruit/`) | ✅ `backend/` |
| Comando | ✅ Correto | ✅ Correto |
| Módulo encontrado | ❌ Não | ✅ Sim |

---

## 💡 Conclusão

O erro ocorre porque o comando está sendo executado do diretório **raiz** ao invés da pasta **backend**.

**Solução:** Execute `cd backend` antes de rodar o uvicorn.

