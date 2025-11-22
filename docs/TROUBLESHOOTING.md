# Guia de Troubleshooting - Amazon Fruit

Este documento ajuda a resolver problemas comuns da aplicação Amazon Fruit.

## 🔍 Diagnóstico Inicial

### Verificar Status da Aplicação

```bash
# Health check
curl http://localhost:8000/api/health

# Verificar logs
docker-compose logs app  # Com Docker
tail -f logs/app.log     # Sem Docker
```

## 🐛 Problemas Comuns

### 1. Aplicação não inicia

#### Sintomas
- Erro ao iniciar uvicorn
- Porta já em uso
- Módulos não encontrados

#### Soluções

**Porta em uso:**
```bash
# Linux/Mac
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Ou usar porta diferente
uvicorn app.main:app --port 8001
```

**Módulos não encontrados:**
```bash
# Verificar ambiente virtual
which python
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstalar dependências
pip install -r backend/requirements.txt
```

### 2. Banco de dados não encontrado

#### Sintomas
- Erro: "Database not found"
- Health check retorna "warning"
- Dashboards não carregam dados

#### Soluções

```bash
# Verificar se arquivo existe
ls -la data/amazon_fruit.db

# Verificar caminho no .env
cat .env | grep DB_PATH

# Criar diretório se não existir
mkdir -p data

# Verificar permissões
chmod 644 data/amazon_fruit.db  # Linux/Mac
```

**Importar dados:**
```bash
python scripts/migrate_excel_to_sqlite.py
```

### 3. Erro 500 - Internal Server Error

#### Sintomas
- Erro 500 em endpoints
- Logs mostram exceções Python

#### Soluções

```bash
# Verificar logs detalhados
docker-compose logs -f app

# Verificar banco de dados
python -c "import sqlite3; conn = sqlite3.connect('data/amazon_fruit.db'); print('OK')"

# Verificar permissões
ls -la data/
```

### 4. CORS Error

#### Sintomas
- Erro no console do navegador
- "CORS policy" bloqueando requisições

#### Soluções

```bash
# Verificar CORS_ORIGINS no .env
cat .env | grep CORS_ORIGINS

# Adicionar origem correta
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000,http://seu-dominio.com
```

### 5. Gráficos não renderizam

#### Sintomas
- Dashboards carregam mas gráficos não aparecem
- Erro no console do navegador

#### Soluções

```bash
# Verificar Plotly.js carregado
# Abrir DevTools > Network > Verificar plotly.min.js

# Verificar dados da API
curl http://localhost:8000/api/charts/financial/evolution?start_date=2020-01-01&end_date=2022-12-31

# Verificar console do navegador para erros JavaScript
```

### 6. Exportação não funciona

#### Sintomas
- Botão de exportar não responde
- Erro ao baixar arquivo

#### Soluções

```bash
# Verificar openpyxl instalado
pip show openpyxl

# Reinstalar se necessário
pip install openpyxl==3.1.2

# Verificar permissões de escrita
touch test.xlsx
rm test.xlsx
```

### 7. Performance lenta

#### Sintomas
- Dashboards demoram para carregar
- Timeout em requisições

#### Soluções

```bash
# Verificar workers do Uvicorn
uvicorn app.main:app --workers 4

# Verificar tamanho do banco
du -h data/amazon_fruit.db

# Otimizar banco SQLite
sqlite3 data/amazon_fruit.db "VACUUM; ANALYZE;"
```

### 8. Docker - Container não inicia

#### Sintomas
- `docker-compose up` falha
- Container para imediatamente

#### Soluções

```bash
# Verificar logs
docker-compose logs app

# Verificar configuração
docker-compose config

# Rebuild completo
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Verificar volumes
docker-compose exec app ls -la /app/data/
```

### 9. Erro de permissão (Linux/Mac)

#### Sintomas
- Permission denied
- Não consegue escrever logs

#### Soluções

```bash
# Dar permissões corretas
chmod +x scripts/*.sh
chmod 644 data/amazon_fruit.db
chmod 755 data/

# Criar diretório de logs
mkdir -p logs
chmod 755 logs
```

### 10. Modo escuro não funciona

#### Sintomas
- Toggle não muda tema
- Preferência não persiste

#### Soluções

```bash
# Verificar localStorage no navegador
# DevTools > Application > Local Storage

# Limpar cache do navegador
# Ctrl+Shift+Delete (Chrome/Firefox)

# Verificar JavaScript carregado
# DevTools > Console > Verificar erros
```

## 🔧 Comandos Úteis

### Verificar Status

```bash
# Health check
curl http://localhost:8000/api/health

# Testar DataHandler
curl http://localhost:8000/api/test/data-handler

# Listar endpoints disponíveis
curl http://localhost:8000/docs
```

### Logs

```bash
# Docker
docker-compose logs -f app
docker-compose logs --tail=100 app

# Sem Docker
tail -f logs/app.log
tail -n 100 logs/app.log
```

### Banco de Dados

```bash
# Verificar integridade
sqlite3 data/amazon_fruit.db "PRAGMA integrity_check;"

# Verificar tabelas
sqlite3 data/amazon_fruit.db ".tables"

# Verificar tamanho
du -h data/amazon_fruit.db

# Backup manual
cp data/amazon_fruit.db backups/backup_$(date +%Y%m%d).db
```

### Limpeza

```bash
# Limpar cache Python
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete

# Limpar logs antigos
find logs/ -name "*.log" -mtime +30 -delete

# Limpar Docker
docker-compose down -v
docker system prune -a
```

## 📊 Verificação de Saúde

### Checklist Rápido

```bash
# 1. Aplicação responde
curl http://localhost:8000/api/health

# 2. Banco de dados existe
test -f data/amazon_fruit.db && echo "OK" || echo "FALTA"

# 3. Dependências instaladas
pip list | grep fastapi

# 4. Porta disponível
lsof -i :8000 || echo "Porta livre"

# 5. Logs sem erros críticos
tail -n 50 logs/app.log | grep -i error
```

## 🆘 Quando Nada Funciona

### Reset Completo

```bash
# 1. Parar tudo
docker-compose down
pkill -f uvicorn

# 2. Limpar ambiente
rm -rf venv
rm -rf __pycache__
rm -rf .pytest_cache

# 3. Recriar ambiente
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# 4. Verificar banco
ls -la data/amazon_fruit.db

# 5. Reiniciar
cd backend
uvicorn app.main:app --reload
```

### Restaurar Backup

```bash
# Parar aplicação
docker-compose down

# Restaurar banco
cp backups/amazon_fruit_YYYYMMDD_HHMMSS.db data/amazon_fruit.db

# Reiniciar
docker-compose up -d
```

## 📞 Obter Ajuda

Se o problema persistir:

1. **Coletar Informações:**
   - Versão do Python: `python --version`
   - Versão do Docker: `docker --version`
   - Logs completos: `docker-compose logs > logs.txt`
   - Saída do health check: `curl http://localhost:8000/api/health`

2. **Verificar Documentação:**
   - `docs/INSTALL.md` - Instalação
   - `docs/DEPLOY.md` - Deploy
   - `docs/README.md` - Visão geral

3. **Criar Issue:**
   - Incluir informações coletadas
   - Descrever passos para reproduzir
   - Incluir logs e screenshots

---

**Última atualização:** 2025-01-XX

