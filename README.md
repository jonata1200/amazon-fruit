# 🍎 Amazon Fruit - Sistema de Análise de Dados

Sistema web moderno para análise de dados empresariais, migrado de aplicação desktop PyQt6.

## ✨ Características

- 📊 **6 Dashboards Interativos** - Geral, Finanças, Estoque, Público-Alvo, Fornecedores, RH
- 📈 **20+ Gráficos Plotly** - Visualizações interativas e responsivas
- 🎨 **Interface Moderna** - Design system completo com modo escuro
- 🔍 **Busca Global** - Busca unificada em todos os dados
- 📤 **Exportação** - Excel, CSV, PNG, SVG, PDF
- ⚡ **Performance** - Cache, compressão, otimizações
- 🔒 **Segurança** - Rate limiting, CORS, validações
- 📱 **Responsivo** - Mobile, tablet e desktop

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.11+
- Docker (opcional)

### Instalação Rápida

```bash
# 1. Clonar repositório
git clone <url-do-repositorio>
cd amazon-fruit

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r backend/requirements.txt

# 4. Iniciar servidor
cd backend
python -m uvicorn app.main:app --reload
```

Acesse: **http://localhost:8000**

### Com Docker

```bash
docker-compose up -d
```

## 📚 Documentação

- **[INSTALL.md](docs/INSTALL.md)** - Guia de instalação detalhado
- **[DEPLOY.md](docs/DEPLOY.md)** - Guia de deploy em produção
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Solução de problemas
- **[DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md)** - Design system da aplicação

## 🏗️ Arquitetura

### Backend
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **Pandas** - Análise de dados
- **Plotly** - Geração de gráficos

### Frontend
- **HTML5/CSS3** - Estrutura e estilos
- **JavaScript (Vanilla)** - Lógica e interatividade
- **Bootstrap 5** - Framework CSS responsivo
- **Plotly.js** - Gráficos interativos

### Banco de Dados
- **SQLite** - Banco de dados leve e portável

## 📁 Estrutura do Projeto

```
amazon-fruit/
├── backend/              # Código backend (FastAPI)
│   ├── app/
│   │   ├── api/         # Rotas da API
│   │   ├── services/    # Lógica de negócio
│   │   ├── utils/       # Utilitários
│   │   └── middleware/  # Middlewares
│   └── requirements.txt
├── frontend/            # Código frontend
│   ├── static/          # CSS, JS, imagens
│   └── templates/       # Templates HTML
├── data/                # Banco de dados e dados Excel
├── docs/                # Documentação
├── scripts/             # Scripts utilitários
├── Dockerfile           # Imagem Docker
├── docker-compose.yml   # Orquestração Docker
└── README.md            # Este arquivo
```

## 🎯 Funcionalidades Principais

### Dashboards

1. **Dashboard Geral**
   - Evolução mensal de faturamento e lucro
   - KPIs financeiros principais

2. **Dashboard Finanças**
   - Receitas, despesas e lucro
   - Top 5 receitas e despesas por categoria

3. **Dashboard Estoque**
   - Produtos mais e menos vendidos
   - Rupturas de estoque

4. **Dashboard Público-Alvo**
   - Distribuição por localização
   - Distribuição por gênero
   - Canais de venda

5. **Dashboard Fornecedores**
   - Ranking de fornecedores
   - Distribuição geográfica

6. **Dashboard RH**
   - Headcount por departamento
   - Custos por departamento
   - Distribuição por cargo

### Funcionalidades Avançadas

- 🔍 **Busca Global** - Busca em todos os dados
- 🔔 **Sistema de Alertas** - Alertas de estoque baixo e problemas financeiros
- 📊 **Filtros Avançados** - Filtros por categoria, tipo, período
- 📈 **Comparação de Períodos** - Compare dois períodos lado a lado
- 🌙 **Modo Escuro** - Tema escuro com persistência
- ⌨️ **Atalhos de Teclado** - Navegação rápida
- 📤 **Exportação** - Exporte dados e gráficos em múltiplos formatos

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz:

```env
ENVIRONMENT=development
DEBUG=True
DB_PATH=./data/amazon_fruit.db
API_HOST=127.0.0.1
API_PORT=8000
CORS_ORIGINS=http://localhost:8000
```

Veja `.env.example` para todas as opções.

## 🐳 Docker

### Build

```bash
docker build -t amazon-fruit .
```

### Run

```bash
docker run -d \
  --name amazon-fruit \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data:ro \
  amazon-fruit
```

### Docker Compose

```bash
docker-compose up -d
```

## 🧪 Testes

```bash
# Health check
curl http://localhost:8000/api/health

# Testar DataHandler
curl http://localhost:8000/api/test/data-handler
```

## 📊 API

A API está documentada em `/docs` quando em modo desenvolvimento.

Principais endpoints:
- `/api/health` - Health check
- `/api/dashboard/{nome}` - Dados do dashboard
- `/api/charts/{tipo}` - Dados dos gráficos
- `/api/export/{tabela}` - Exportar dados
- `/api/search` - Busca global
- `/api/alerts` - Alertas do sistema

## 🔒 Segurança

- Rate limiting configurável
- CORS restritivo em produção
- Validação de inputs
- Headers de segurança
- Logs estruturados

## 📈 Performance

- Compressão GZip
- Cache no frontend (localStorage)
- Otimizações de queries
- Workers configuráveis

## 🛠️ Desenvolvimento

### Scripts Úteis

```bash
# Iniciar servidor rápido (Windows)
.\start-server-quick.ps1

# Iniciar servidor (Linux/Mac)
./start-server.sh

# Backup do banco
./scripts/backup_database.sh
```

### Estrutura de Código

- **Backend**: `backend/app/`
- **Frontend**: `frontend/`
- **Documentação**: `docs/`

## 📝 Changelog

### Fase 6 - Deploy e Produção
- ✅ Docker e Docker Compose
- ✅ Configuração Nginx
- ✅ Sistema de logging
- ✅ Rate limiting
- ✅ Scripts de backup
- ✅ Documentação completa

### Fase 5 - Interface e UX
- ✅ Design system completo
- ✅ Modo escuro
- ✅ Ícones Font Awesome
- ✅ Responsividade completa
- ✅ Acessibilidade

### Fase 4 - Funcionalidades Avançadas
- ✅ Exportação de dados e gráficos
- ✅ Busca global
- ✅ Sistema de alertas
- ✅ Filtros avançados
- ✅ Comparação de períodos

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é privado e proprietário.

## 📞 Suporte

- **Documentação**: `docs/`
- **Troubleshooting**: `docs/TROUBLESHOOTING.md`
- **Issues**: [GitHub Issues](link-para-issues)

## 🙏 Agradecimentos

- FastAPI pela excelente framework
- Plotly pelos gráficos interativos
- Bootstrap pela base responsiva
- Font Awesome pelos ícones

---

**Desenvolvido com ❤️ para análise de dados empresariais**

**Versão:** 1.0.0  
**Última atualização:** 2025-01-XX

