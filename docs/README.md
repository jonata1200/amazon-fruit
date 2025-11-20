# Plano de Migração: Desktop para Web

## Visão Geral do Projeto

O **Amazon Fruit** é uma aplicação desktop desenvolvida em Python com PyQt6 que gerencia e analisa dados de uma empresa de frutas. A aplicação possui:

- **7 Dashboards** interativos (Geral, Estoque, Finanças, Público-Alvo, Fornecedores, Recursos Humanos, Insights)
- **5 Módulos de Análise** de dados (financeira, estoque, fornecedores, público-alvo, RH)
- **Geração de Relatórios PDF** completos
- **Banco de dados SQLite** para armazenamento
- **Visualizações** com matplotlib/seaborn

## Objetivo da Migração

Transformar a aplicação desktop em uma **aplicação web moderna**, mantendo toda a funcionalidade existente e aproveitando as vantagens da arquitetura web:

- Acesso multiplataforma (qualquer dispositivo com navegador)
- Atualizações centralizadas
- Melhor experiência de usuário com interfaces responsivas
- Facilidade de compartilhamento e colaboração

## Tecnologias Propostas

### Backend
- **FastAPI** ou **Flask** - Framework web Python
- **SQLAlchemy** - ORM para acesso ao banco de dados
- **Pandas** - Mantido para análises de dados
- **Plotly** - Substituição do matplotlib para gráficos interativos web

### Frontend
- **HTML5/CSS3/JavaScript** - Base da interface
- **Bootstrap** ou **Tailwind CSS** - Framework CSS responsivo
- **Chart.js** ou **Plotly.js** - Visualizações interativas no cliente
- **Vue.js** ou **React** (opcional) - Para interfaces mais dinâmicas

### Infraestrutura
- **Gunicorn** ou **Uvicorn** - Servidor WSGI/ASGI
- **Nginx** - Servidor web reverso (produção)
- **Docker** (opcional) - Containerização

## Estrutura do Plano

O plano está dividido em **6 fases** progressivas:

1. **[Fase 1: Preparação e Arquitetura Base](fase-01-preparacao.md)**
   - Análise detalhada do código existente
   - Definição da arquitetura web
   - Setup do ambiente de desenvolvimento

2. **[Fase 2: API Backend](fase-02-api-backend.md)**
   - Criação da API REST
   - Migração do DataHandler
   - Endpoints para dados e análises

3. **[Fase 3: Migração dos Dashboards](fase-03-dashboards.md)**
   - Conversão dos dashboards PyQt6 para HTML
   - Implementação de gráficos web interativos
   - Sistema de navegação

4. **[Fase 4: Funcionalidades Avançadas](fase-04-funcionalidades.md)**
   - Sistema de filtros de período
   - Geração de relatórios PDF via web
   - KPIs e widgets interativos

5. **[Fase 5: Interface e UX](fase-05-interface.md)**
   - Design responsivo
   - Melhorias de usabilidade
   - Otimizações de performance

6. **[Fase 6: Deploy e Produção](fase-06-deploy.md)**
   - Configuração de servidor
   - Testes finais
   - Documentação de usuário

## Princípios da Migração

1. **Manter funcionalidades existentes** - Nenhuma feature será perdida
2. **Reutilizar código Python** - Módulos de análise serão mantidos
3. **Melhorar experiência** - Aproveitar recursos web nativos
4. **Código limpo** - Seguir boas práticas de desenvolvimento web
5. **Documentação** - Documentar todas as mudanças

## Estimativa de Tempo

- **Fase 1**: 1-2 semanas
- **Fase 2**: 2-3 semanas
- **Fase 3**: 3-4 semanas
- **Fase 4**: 2-3 semanas
- **Fase 5**: 2 semanas
- **Fase 6**: 1-2 semanas

**Total estimado**: 11-16 semanas (3-4 meses)

## Próximos Passos

Comece pela [Fase 1: Preparação e Arquitetura Base](fase-01-preparacao.md) para entender em detalhes o que será feito na primeira etapa da migração.

