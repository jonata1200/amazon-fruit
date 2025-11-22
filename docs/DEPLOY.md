# Guia de Deploy - Amazon Fruit

Este documento descreve como fazer o deploy da aplicação Amazon Fruit em produção.

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.11+ (para desenvolvimento local)
- Acesso ao servidor de produção
- Domínio configurado (opcional, para HTTPS)

## 🚀 Opções de Deploy

### Opção 1: Deploy com Docker (Recomendado)

#### 1.1 Preparação

```bash
# Clonar repositório
git clone <seu-repositorio>
cd amazon-fruit

# Copiar arquivo de ambiente
cp .env.production.example .env.production
# Editar .env.production com suas configurações
```

#### 1.2 Configurar Variáveis de Ambiente

Edite o arquivo `.env.production`:

```env
ENVIRONMENT=production
DEBUG=False
DB_PATH=/app/data/amazon_fruit.db
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://seu-dominio.com
SECRET_KEY=<gere-uma-chave-secreta-aleatoria>
```

**Gerar chave secreta:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 1.3 Build e Iniciar

```bash
# Build da imagem
docker-compose build

# Iniciar serviços
docker-compose up -d

# Verificar logs
docker-compose logs -f app
```

#### 1.4 Verificar Status

```bash
# Health check
curl http://localhost:8000/api/health

# Verificar containers
docker-compose ps
```

### Opção 2: Deploy Manual (Sem Docker)

#### 2.1 Instalar Dependências

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r backend/requirements.txt
```

#### 2.2 Configurar Ambiente

```bash
# Copiar arquivo de ambiente
cp .env.production.example .env.production
# Editar .env.production
```

#### 2.3 Iniciar Aplicação

```bash
# Desenvolvimento
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Produção (com workers)
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level warning
```

### Opção 3: Deploy em Serviços Cloud

#### 3.1 Railway

1. Conectar repositório GitHub
2. Configurar variáveis de ambiente
3. Railway detecta Dockerfile automaticamente
4. Deploy automático a cada push

#### 3.2 Render

1. Criar novo Web Service
2. Conectar repositório
3. Configurar:
   - Build Command: `docker build -t amazon-fruit .`
   - Start Command: `docker run -p 8000:8000 amazon-fruit`
4. Adicionar variáveis de ambiente

#### 3.3 Heroku

1. Instalar Heroku CLI
2. Criar `Procfile`:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
3. Deploy:
   ```bash
   heroku create amazon-fruit
   heroku config:set ENVIRONMENT=production
   git push heroku main
   ```

## 🔒 Configuração SSL/TLS

### Com Let's Encrypt (Nginx)

```bash
# Instalar certbot
sudo apt-get install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com

# Renovação automática
sudo certbot renew --dry-run
```

### Com Docker e Certbot

```yaml
# Adicionar ao docker-compose.yml
services:
  certbot:
    image: certbot/certbot
    volumes:
      - ./nginx/ssl:/etc/letsencrypt
      - ./nginx/conf.d:/etc/nginx/conf.d
    command: certonly --webroot -w /var/www/certbot -d seu-dominio.com
```

## 📊 Monitoramento

### Health Check

```bash
# Verificar saúde da aplicação
curl http://localhost:8000/api/health

# Resposta esperada:
{
  "status": "healthy",
  "timestamp": "2025-01-XX...",
  "version": "1.0.0",
  "environment": "production",
  "checks": {
    "database": {
      "status": "healthy",
      "path": "/app/data/amazon_fruit.db",
      "exists": true
    }
  }
}
```

### Logs

```bash
# Docker
docker-compose logs -f app

# Logs do sistema
tail -f logs/app.log
```

## 🔄 Atualizações

### Com Docker

```bash
# Pull das mudanças
git pull

# Rebuild e restart
docker-compose up -d --build

# Verificar status
docker-compose ps
```

### Manual

```bash
# Pull das mudanças
git pull

# Atualizar dependências
pip install -r backend/requirements.txt --upgrade

# Reiniciar aplicação
# (usar systemd, supervisor, ou PM2)
```

## 💾 Backup do Banco de Dados

### Automático (Cron)

```bash
# Adicionar ao crontab
0 2 * * * /caminho/para/scripts/backup_database.sh
```

### Manual

```bash
# Linux/Mac
./scripts/backup_database.sh

# Windows
powershell -File scripts/backup_database.ps1
```

## 🛠️ Troubleshooting

### Problema: Container não inicia

```bash
# Verificar logs
docker-compose logs app

# Verificar configurações
docker-compose config

# Rebuild completo
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Banco de dados não encontrado

```bash
# Verificar caminho
docker-compose exec app ls -la /app/data/

# Verificar permissões
docker-compose exec app ls -la /app/data/amazon_fruit.db
```

### Problema: Porta já em uso

```bash
# Verificar processos
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Alterar porta no docker-compose.yml
ports:
  - "8001:8000"  # Usar porta diferente
```

## 📝 Checklist de Deploy

- [ ] Variáveis de ambiente configuradas
- [ ] Chave secreta gerada
- [ ] CORS configurado corretamente
- [ ] Banco de dados acessível
- [ ] SSL/TLS configurado (se aplicável)
- [ ] Health check funcionando
- [ ] Logs configurados
- [ ] Backup automático configurado
- [ ] Monitoramento ativo
- [ ] Documentação atualizada

## 🔐 Segurança

### Checklist de Segurança

- [ ] `DEBUG=False` em produção
- [ ] `SECRET_KEY` única e segura
- [ ] CORS restritivo
- [ ] Rate limiting habilitado
- [ ] HTTPS configurado
- [ ] Headers de segurança (Nginx)
- [ ] Logs não expõem informações sensíveis
- [ ] Backup criptografado (opcional)

## 📞 Suporte

Para problemas ou dúvidas:
1. Verificar logs da aplicação
2. Consultar `docs/TROUBLESHOOTING.md`
3. Verificar health check endpoint
4. Revisar configurações de ambiente

---

**Última atualização:** 2025-01-XX

