# Guia de Teste no Navegador - Fase 1

Este guia explica passo a passo como testar a aplicação web no navegador.

## 📋 Pré-requisitos

- Python 3.8+ instalado
- Ambiente virtual criado (ou criar agora)
- Terminal/PowerShell aberto no diretório do projeto

## 🚀 Passo a Passo

### Passo 1: Ativar Ambiente Virtual

Abra o terminal/PowerShell no diretório do projeto (`amazon-fruit`) e execute:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

Você deve ver `(venv)` no início da linha do terminal, indicando que o ambiente está ativo.

> **Nota:** Se ainda não criou o ambiente virtual, execute primeiro:
> ```bash
> python -m venv venv
> ```

### Passo 2: Instalar Dependências

Ainda no terminal, navegue para a pasta `backend` e instale as dependências:

```bash
cd backend
pip install -r requirements.txt
```

Isso vai instalar:
- FastAPI
- Uvicorn
- Pandas
- Plotly
- E outras dependências necessárias

**Tempo estimado:** 2-5 minutos (dependendo da velocidade da internet)

### Passo 3: Verificar Instalação (Opcional)

Antes de iniciar o servidor, você pode testar se tudo está configurado corretamente:

```bash
python test_setup.py
```

Você deve ver:
```
[OK] Estrutura: [OK] PASSOU
[OK] Configurações: [OK] PASSOU
[OK] Imports: [OK] PASSOU
```

### Passo 4: Iniciar o Servidor

Ainda na pasta `backend`, execute:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Você deve ver uma saída similar a:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**⚠️ IMPORTANTE:** Mantenha este terminal aberto! O servidor precisa estar rodando para acessar no navegador.

### Passo 5: Abrir no Navegador

Com o servidor rodando, abra seu navegador (Chrome, Firefox, Edge, etc.) e acesse:

#### 5.1 Página Inicial
```
http://localhost:8000/
```

**O que você deve ver:**
- Título "🍎 Amazon Fruit"
- Mensagem "✅ Frontend Configurado com Sucesso!"
- Status da API mostrando "healthy" (verde)

#### 5.2 Health Check da API
```
http://localhost:8000/api/health
```

**O que você deve ver:**
```json
{
  "status": "healthy",
  "message": "API está funcionando corretamente"
}
```

#### 5.3 Documentação Swagger (Interativa)
```
http://localhost:8000/docs
```

**O que você deve ver:**
- Interface interativa do Swagger UI
- Lista de endpoints disponíveis:
  - `GET /` - Página inicial
  - `GET /api/health` - Health check
- Botão "Try it out" para testar endpoints diretamente

#### 5.4 Documentação ReDoc (Alternativa)
```
http://localhost:8000/redoc
```

**O que você deve ver:**
- Documentação alternativa em formato ReDoc
- Mais limpa e organizada

## ✅ Checklist de Verificação

Marque cada item conforme verificar:

- [ ] Servidor inicia sem erros no terminal
- [ ] Página inicial (http://localhost:8000/) carrega
- [ ] Mensagem de sucesso aparece na página inicial
- [ ] Status da API mostra "healthy" (verde)
- [ ] Health check (http://localhost:8000/api/health) retorna JSON correto
- [ ] Swagger UI (http://localhost:8000/docs) abre corretamente
- [ ] Endpoints aparecem listados no Swagger
- [ ] É possível testar o endpoint `/api/health` pelo Swagger

## 🐛 Solução de Problemas

### Problema: "uvicorn não é reconhecido como comando"

**Solução:**
```bash
pip install uvicorn[standard]
```

### Problema: "ModuleNotFoundError: No module named 'fastapi'"

**Solução:**
```bash
pip install -r requirements.txt
```

### Problema: "Address already in use" (porta 8000 ocupada)

**Solução 1:** Parar o processo que está usando a porta
```bash
# Windows - encontrar processo na porta 8000
netstat -ano | findstr :8000
# Depois matar o processo (substituir PID pelo número encontrado)
taskkill /PID <PID> /F
```

**Solução 2:** Usar outra porta
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```
E acesse: http://localhost:8001/

### Problema: Página não carrega / Erro 404

**Verifique:**
1. Servidor está rodando? (veja o terminal)
2. Está acessando a URL correta? (http://localhost:8000/)
3. Não há erros no terminal do servidor?

### Problema: "CORS" ou erros de acesso

**Solução:** Isso não deve acontecer nesta fase, mas se acontecer, verifique o arquivo `backend/app/config.py` e adicione sua URL na lista de `cors_origins`.

## 📸 O que Esperar Ver

### Página Inicial (http://localhost:8000/)
- Fundo branco com container centralizado
- Título "🍎 Amazon Fruit" em roxo (#6A0DAD)
- Caixa verde com mensagem de sucesso
- Caixa roxa com informações da API
- Status "healthy" em verde

### Swagger UI (http://localhost:8000/docs)
- Interface moderna com fundo escuro
- Lista de endpoints à esquerda
- Documentação detalhada de cada endpoint
- Botão "Try it out" para testar
- Botão "Execute" para fazer requisições

## 🎯 Próximos Passos

Após confirmar que tudo está funcionando:

1. ✅ Teste concluído com sucesso
2. ➡️ Próxima etapa: Migração do DataHandler
3. ➡️ Depois: Criação dos endpoints da API

## 💡 Dicas

- **Modo Reload:** O servidor está rodando com `--reload`, então qualquer mudança no código Python será recarregada automaticamente
- **Parar o Servidor:** Pressione `CTRL+C` no terminal onde o servidor está rodando
- **Logs:** Todos os erros e requisições aparecem no terminal do servidor
- **Testar Endpoints:** Use o Swagger UI para testar endpoints sem precisar de ferramentas externas

## 📞 Precisa de Ajuda?

Se encontrar algum problema não listado aqui:
1. Verifique os logs no terminal do servidor
2. Verifique se todas as dependências foram instaladas
3. Certifique-se de que está na pasta `backend` ao executar os comandos

