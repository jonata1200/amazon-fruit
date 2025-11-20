# Fase 6: Deploy e Produção

## Objetivo

Preparar a aplicação para produção, configurar servidor, realizar testes finais e garantir que tudo esteja funcionando corretamente em ambiente de produção.

## Duração Estimada

**1-2 semanas**

## Tarefas Detalhadas

### 6.1 Preparação para Produção

#### 6.1.1 Variáveis de Ambiente

**Arquivo:** `.env.production`

**Variáveis necessárias:**
```env
# Ambiente
ENVIRONMENT=production
DEBUG=False

# Banco de Dados
DB_PATH=/app/data/amazon_fruit.db

# API
API_HOST=0.0.0.0
API_PORT=8000

# CORS
CORS_ORIGINS=https://seu-dominio.com

# Segurança
SECRET_KEY=gerar-chave-secreta-aleatoria
```

**Tarefas:**
- [ ] Criar arquivo `.env.production`
- [ ] Documentar todas as variáveis
- [ ] Gerar chaves secretas
- [ ] Configurar CORS adequadamente

#### 6.1.2 Configurações de Segurança

**Melhorias de segurança:**
- [ ] Desabilitar debug em produção
- [ ] Configurar CORS restritivo
- [ ] Adicionar rate limiting
- [ ] Configurar HTTPS
- [ ] Validar inputs rigorosamente
- [ ] Sanitizar outputs

**Tarefas:**
- [ ] Revisar configurações de segurança
- [ ] Implementar rate limiting
- [ ] Configurar HTTPS
- [ ] Adicionar validações extras

#### 6.1.3 Logging

**Configuração:**
- [ ] Logs estruturados
- [ ] Níveis de log apropriados
- [ ] Rotação de logs
- [ ] Monitoramento de erros

**Tarefas:**
- [ ] Configurar sistema de logging
- [ ] Definir níveis de log
- [ ] Implementar rotação de logs
- [ ] Integrar com serviço de monitoramento (opcional)

### 6.2 Containerização (Docker)

#### 6.2.1 Dockerfile

**Arquivo:** `Dockerfile`

**Estrutura:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY backend/ /app/
COPY data/ /app/data/

# Expor porta
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Tarefas:**
- [ ] Criar Dockerfile otimizado
- [ ] Usar multi-stage build (opcional)
- [ ] Otimizar tamanho da imagem
- [ ] Testar build localmente

#### 6.2.2 Docker Compose

**Arquivo:** `docker-compose.yml`

**Serviços:**
- Aplicação FastAPI
- Nginx (opcional)
- Redis (opcional, para cache)

**Tarefas:**
- [ ] Criar docker-compose.yml
- [ ] Configurar serviços
- [ ] Testar localmente
- [ ] Documentar uso

### 6.3 Servidor Web

#### 6.3.1 Escolha do Servidor WSGI/ASGI

**Opções:**
- **Uvicorn** (recomendado para FastAPI)
- **Gunicorn** com workers Uvicorn
- **Hypercorn**

**Configuração Uvicorn:**
```bash
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info
```

**Tarefas:**
- [ ] Escolher servidor
- [ ] Configurar workers
- [ ] Testar performance
- [ ] Documentar configuração

#### 6.3.2 Nginx como Reverse Proxy

**Configuração Nginx:**

**Arquivo:** `nginx.conf`

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    # Redirecionar para HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name seu-dominio.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Proxy para aplicação
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Arquivos estáticos
    location /static {
        alias /path/to/frontend/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

**Tarefas:**
- [ ] Configurar Nginx
- [ ] Configurar SSL/TLS
- [ ] Otimizar cache de arquivos estáticos
- [ ] Testar configuração

### 6.4 Banco de Dados

#### 6.4.1 Backup e Migração

**Tarefas:**
- [ ] Criar script de backup do SQLite
- [ ] Documentar processo de backup
- [ ] Testar restauração
- [ ] Configurar backups automáticos

**Script de backup:**
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_PATH="/app/data/amazon_fruit.db"

cp "$DB_PATH" "$BACKUP_DIR/amazon_fruit_$DATE.db"
```

#### 6.4.2 Otimizações

**Tarefas:**
- [ ] Criar índices necessários
- [ ] Analisar queries lentas
- [ ] Otimizar queries
- [ ] Configurar VACUUM periódico

### 6.5 Testes Finais

#### 6.5.1 Testes de Integração

**Checklist:**
- [ ] Todos os endpoints funcionando
- [ ] Todos os dashboards carregando
- [ ] Gráficos renderizando corretamente
- [ ] Filtros funcionando
- [ ] Exportações funcionando
- [ ] Relatórios gerando corretamente

**Tarefas:**
- [ ] Criar checklist de testes
- [ ] Executar todos os testes
- [ ] Documentar resultados
- [ ] Corrigir problemas encontrados

#### 6.5.2 Testes de Performance

**Métricas:**
- Tempo de resposta da API
- Tempo de carregamento das páginas
- Uso de memória
- Uso de CPU

**Tarefas:**
- [ ] Realizar testes de carga
- [ ] Medir performance
- [ ] Identificar gargalos
- [ ] Otimizar onde necessário

#### 6.5.3 Testes de Segurança

**Checklist:**
- [ ] Validação de inputs
- [ ] Proteção contra SQL injection
- [ ] Proteção contra XSS
- [ ] CORS configurado corretamente
- [ ] HTTPS funcionando
- [ ] Headers de segurança

**Tarefas:**
- [ ] Realizar testes de segurança
- [ ] Usar ferramentas automatizadas
- [ ] Corrigir vulnerabilidades
- [ ] Documentar medidas de segurança

### 6.6 Monitoramento

#### 6.6.1 Health Checks

**Endpoint:**
```python
@router.get("/health")
async def health_check():
    """
    Endpoint de health check para monitoramento.
    """
    return {
        "status": "healthy",
        "database": check_database(),
        "timestamp": datetime.now().isoformat()
    }
```

**Tarefas:**
- [ ] Criar endpoint de health check
- [ ] Verificar conectividade com banco
- [ ] Retornar status adequado

#### 6.6.2 Monitoramento de Erros

**Ferramentas opcionais:**
- Sentry
- Rollbar
- LogRocket

**Tarefas:**
- [ ] Escolher ferramenta (opcional)
- [ ] Integrar monitoramento
- [ ] Configurar alertas

#### 6.6.3 Métricas

**Métricas importantes:**
- Requisições por segundo
- Tempo de resposta
- Taxa de erro
- Uso de recursos

**Tarefas:**
- [ ] Configurar coleta de métricas
- [ ] Criar dashboard de monitoramento (opcional)
- [ ] Configurar alertas

### 6.7 Documentação

#### 6.7.1 Documentação Técnica

**Arquivos:**
- [ ] README.md principal
- [ ] INSTALL.md (instruções de instalação)
- [ ] DEPLOY.md (instruções de deploy)
- [ ] API.md (documentação da API)
- [ ] TROUBLESHOOTING.md (solução de problemas)

**Tarefas:**
- [ ] Criar documentação completa
- [ ] Incluir exemplos
- [ ] Adicionar screenshots
- [ ] Manter atualizada

#### 6.7.2 Documentação do Usuário

**Conteúdo:**
- [ ] Guia de uso básico
- [ ] Explicação de cada dashboard
- [ ] Como usar filtros
- [ ] Como gerar relatórios
- [ ] FAQ

**Tarefas:**
- [ ] Criar guia do usuário
- [ ] Adicionar screenshots
- [ ] Criar vídeo tutorial (opcional)

### 6.8 Deploy

#### 6.8.1 Escolha da Plataforma

**Opções:**
- **Servidor próprio** (VPS)
- **Cloud providers** (AWS, Google Cloud, Azure)
- **Platform as a Service** (Heroku, Railway, Render)

**Tarefas:**
- [ ] Escolher plataforma
- [ ] Configurar ambiente
- [ ] Realizar deploy
- [ ] Testar em produção

#### 6.8.2 Processo de Deploy

**Checklist:**
- [ ] Código versionado (Git)
- [ ] Testes passando
- [ ] Build funcionando
- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados migrado
- [ ] Servidor configurado
- [ ] SSL/TLS configurado
- [ ] Monitoramento ativo

**Tarefas:**
- [ ] Criar script de deploy
- [ ] Automatizar processo (opcional)
- [ ] Documentar processo
- [ ] Testar deploy

### 6.9 CI/CD (Opcional)

#### 6.9.1 Pipeline de CI/CD

**Ferramentas:**
- GitHub Actions
- GitLab CI
- Jenkins

**Etapas:**
1. Lint e formatação
2. Testes unitários
3. Testes de integração
4. Build
5. Deploy (se testes passarem)

**Tarefas:**
- [ ] Configurar pipeline
- [ ] Adicionar testes automatizados
- [ ] Configurar deploy automático (opcional)

### 6.10 Manutenção

#### 6.10.1 Plano de Manutenção

**Tarefas regulares:**
- [ ] Atualizar dependências
- [ ] Revisar logs
- [ ] Verificar backups
- [ ] Monitorar performance
- [ ] Aplicar patches de segurança

**Tarefas:**
- [ ] Criar plano de manutenção
- [ ] Agendar tarefas regulares
- [ ] Documentar procedimentos

## Entregas da Fase 6

- [ ] Aplicação rodando em produção
- [ ] Servidor configurado e seguro
- [ ] SSL/TLS configurado
- [ ] Monitoramento ativo
- [ ] Backups configurados
- [ ] Documentação completa
- [ ] Testes finais realizados
- [ ] Performance aceitável
- [ ] Segurança garantida

## Critérios de Aceitação

1. ✅ Aplicação acessível via HTTPS
2. ✅ Performance aceitável em produção (< 2s tempo de resposta)
3. ✅ Todos os testes passando
4. ✅ Segurança configurada adequadamente
5. ✅ Monitoramento funcionando
6. ✅ Backups configurados
7. ✅ Documentação completa
8. ✅ Aplicação estável e confiável

## Próximos Passos

Após completar todas as fases:

1. **Coletar feedback** dos usuários
2. **Monitorar** uso e performance
3. **Iterar** com melhorias baseadas em feedback
4. **Manter** aplicação atualizada
5. **Expandir** funcionalidades conforme necessário

## Conclusão

Com a conclusão desta fase, a migração do Amazon Fruit de desktop para web estará completa. A aplicação estará pronta para uso em produção, com todas as funcionalidades da versão desktop preservadas e melhoradas, além de novos recursos aproveitando as capacidades da web.

