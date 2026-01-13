# 🚀 Plano de Migração: React + Next.js + TypeScript

## 📋 Visão Geral do Projeto

Este documento descreve o plano completo de migração do sistema Amazon Fruit da arquitetura atual (FastAPI + HTML/CSS/JavaScript) para uma arquitetura moderna baseada em **React + Next.js + TypeScript**.

---

## 🎯 Objetivos da Migração

### Objetivos Principais
- ✅ **Modernizar o Frontend**: Adotar React como biblioteca de UI
- ✅ **Type Safety**: Implementar TypeScript para maior segurança e manutenibilidade
- ✅ **SSR e Performance**: Aproveitar Next.js para Server-Side Rendering e otimizações
- ✅ **Componentização**: Criar componentes reutilizáveis e testáveis
- ✅ **Manutenibilidade**: Melhorar a estrutura e organização do código
- ✅ **Developer Experience**: Tooling moderno com TypeScript, ESLint, Prettier

### Benefícios Esperados
- 🚀 **Performance**: Melhor performance com SSR, Code Splitting e otimizações automáticas
- 🔧 **Manutenção**: Código mais fácil de manter com TypeScript e componentização
- 📱 **Responsividade**: Melhor suporte para Progressive Web App (PWA)
- 🧪 **Testabilidade**: Testes mais fáceis com componentes isolados
- 🎨 **UI/UX**: Componentes reutilizáveis e design system consistente

---

## 📊 Análise da Arquitetura Atual

### Backend (Mantido)
- **Framework**: FastAPI (Python 3.11+)
- **Banco de Dados**: SQLite com SQLAlchemy
- **API**: RESTful endpoints já estruturados
- **Funcionalidades**:
  - 6 dashboards (Geral, Finanças, Estoque, Público-Alvo, Fornecedores, RH)
  - Sistema de alertas
  - Exportação de relatórios (PDF, Excel)
  - Busca global
  - Comparação de períodos

### Frontend (A Migrar)
- **Arquitetura Atual**: HTML templates + Vanilla JavaScript
- **Estrutura**:
  - 6 templates HTML de dashboards
  - 6 módulos JavaScript correspondentes
  - Sistema modular (core, modules, utils, dashboards)
  - CSS organizado por componentes
- **Bibliotecas**: Bootstrap 5, Font Awesome, Plotly.js

---

## 🗺️ Estrutura do Plano de Migração

O plano está dividido em **8 fases sequenciais**, cada uma com seu próprio arquivo de documentação e checklist detalhado:

### [Fase 1: Preparação e Setup Inicial](./MIGRATION_PHASE_1.md)
- Configuração do ambiente Next.js
- Estrutura de pastas e arquitetura
- Configuração de ferramentas (TypeScript, ESLint, Prettier)
- Setup de bibliotecas base

### [Fase 2: Infraestrutura e Configurações](./MIGRATION_PHASE_2.md)
- Configuração de API client com Axios/Fetch
- Sistema de gerenciamento de estado (Context API ou Zustand)
- Sistema de roteamento
- Configuração de temas (dark/light mode)
- Sistema de cache

### [Fase 3: Componentes Base e Design System](./MIGRATION_PHASE_3.md)
- Criação de componentes de UI base
- Sistema de design e variáveis de estilo
- Layout principal (Sidebar, Header, Footer)
- Componentes de navegação
- Sistema de notificações/toast

### [Fase 4: Dashboards - Parte 1](./MIGRATION_PHASE_4.md)
- Dashboard Geral
- Dashboard de Finanças
- Componentes de KPI
- Componentes de gráficos (Plotly ou Recharts)
- Sistema de filtros de período

### [Fase 5: Dashboards - Parte 2](./MIGRATION_PHASE_5.md)
- Dashboard de Estoque
- Dashboard de Público-Alvo
- Dashboard de Fornecedores
- Dashboard de Recursos Humanos

### [Fase 6: Funcionalidades Avançadas](./MIGRATION_PHASE_6.md)
- Sistema de alertas
- Busca global
- Comparação de períodos
- Exportação de relatórios
- Atalhos de teclado
- Modo responsivo/mobile

### [Fase 7: Integração e Testes](./MIGRATION_PHASE_7.md)
- Testes unitários (Jest + React Testing Library)
- Testes de integração
- Testes end-to-end (Playwright/Cypress)
- Validação de performance
- Testes de acessibilidade

### [Fase 8: Deploy e Otimização](./MIGRATION_PHASE_8.md)
- Otimização de bundle
- Configuração de PWA
- SEO e meta tags
- Docker setup
- CI/CD pipeline
- Documentação final
- Migração de produção

---

## 🛠️ Stack Tecnológica Nova

### Core
- **React**: 18.x (biblioteca UI)
- **Next.js**: 14.x (framework React com SSR)
- **TypeScript**: 5.x (linguagem tipada)

### UI e Estilização
- **Tailwind CSS**: Framework CSS utility-first (ou Styled Components)
- **Radix UI** ou **Shadcn/ui**: Componentes acessíveis headless
- **Lucide React**: Ícones (substituto do Font Awesome)
- **Recharts** ou **Plotly.js**: Gráficos interativos

### Estado e Dados
- **Zustand** ou **Context API**: Gerenciamento de estado
- **TanStack Query** (React Query): Cache e sincronização de dados
- **Axios**: Cliente HTTP

### Testes
- **Jest**: Framework de testes
- **React Testing Library**: Testes de componentes
- **Playwright** ou **Cypress**: Testes E2E

### Ferramentas de Desenvolvimento
- **ESLint**: Linting
- **Prettier**: Formatação de código
- **Husky**: Git hooks
- **Commitlint**: Padronização de commits

---

## 📅 Cronograma Estimado

| Fase | Descrição | Duração Estimada | Complexidade |
|------|-----------|------------------|--------------|
| 1 | Preparação e Setup | 2-3 dias | Baixa |
| 2 | Infraestrutura | 3-5 dias | Média |
| 3 | Componentes Base | 5-7 dias | Média |
| 4 | Dashboards Parte 1 | 7-10 dias | Alta |
| 5 | Dashboards Parte 2 | 7-10 dias | Alta |
| 6 | Funcionalidades Avançadas | 5-7 dias | Alta |
| 7 | Integração e Testes | 5-7 dias | Média |
| 8 | Deploy e Otimização | 3-5 dias | Média |
| **Total** | **Projeto Completo** | **37-54 dias** | **6-8 semanas** |

> **Nota**: Os prazos são estimativas e podem variar de acordo com a experiência da equipe e recursos disponíveis.

---

## 🔄 Estratégia de Migração

### Abordagem Recomendada: **Gradual e Incremental**

1. **Desenvolvimento Paralelo**: Manter o sistema atual funcionando enquanto desenvolve o novo
2. **Feature por Feature**: Migrar um dashboard de cada vez
3. **Testes Contínuos**: Validar cada funcionalidade migrada
4. **Rollback Seguro**: Possibilidade de voltar ao sistema anterior se necessário

### Opções de Deploy

#### Opção 1: Big Bang (Não Recomendado)
- Migrar tudo de uma vez
- **Risco**: Alto
- **Downtime**: Potencialmente longo

#### Opção 2: Gradual com Feature Flags (Recomendado)
- Deploy gradual por funcionalidade
- **Risco**: Baixo
- **Downtime**: Mínimo

#### Opção 3: Blue-Green Deployment
- Dois ambientes paralelos
- **Risco**: Médio
- **Downtime**: Zero

---

## 📁 Estrutura de Pastas Proposta

```
amazon-fruit-nextjs/
├── src/
│   ├── app/                      # App Router do Next.js 14
│   │   ├── (dashboards)/        # Grupo de rotas para dashboards
│   │   │   ├── geral/
│   │   │   ├── financas/
│   │   │   ├── estoque/
│   │   │   ├── publico-alvo/
│   │   │   ├── fornecedores/
│   │   │   └── recursos-humanos/
│   │   ├── layout.tsx           # Layout raiz
│   │   ├── page.tsx             # Página inicial
│   │   └── globals.css          # Estilos globais
│   │
│   ├── components/              # Componentes React
│   │   ├── ui/                  # Componentes base (botões, inputs, etc)
│   │   ├── layouts/             # Layouts (Sidebar, Header, Footer)
│   │   ├── dashboards/          # Componentes específicos de dashboards
│   │   ├── charts/              # Componentes de gráficos
│   │   └── features/            # Features complexas (Alerts, Search, etc)
│   │
│   ├── lib/                     # Bibliotecas e utilitários
│   │   ├── api/                 # Cliente da API
│   │   ├── hooks/               # Custom hooks
│   │   ├── utils/               # Funções utilitárias
│   │   └── constants/           # Constantes
│   │
│   ├── store/                   # Estado global (Zustand/Context)
│   │   ├── slices/              # Slices de estado
│   │   └── index.ts             # Store principal
│   │
│   ├── types/                   # Tipos TypeScript
│   │   ├── api.ts               # Tipos da API
│   │   ├── dashboard.ts         # Tipos de dashboards
│   │   └── index.ts             # Exports centralizados
│   │
│   └── styles/                  # Estilos adicionais
│       └── theme.ts             # Tema e variáveis
│
├── public/                      # Arquivos estáticos
│   ├── images/
│   └── icons/
│
├── tests/                       # Testes
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── .next/                       # Build do Next.js (gerado)
├── node_modules/                # Dependências (gerado)
│
├── .env.local                   # Variáveis de ambiente local
├── .eslintrc.json              # Configuração ESLint
├── .prettierrc                  # Configuração Prettier
├── next.config.js              # Configuração Next.js
├── tsconfig.json               # Configuração TypeScript
├── tailwind.config.js          # Configuração Tailwind
├── package.json                # Dependências npm
└── README.md                   # Documentação
```

---

## ⚠️ Riscos e Mitigações

### Riscos Identificados

1. **Performance de Gráficos**
   - **Risco**: Plotly.js pode ter problemas de performance no React
   - **Mitigação**: Considerar Recharts ou Victory, ou otimizar Plotly com React.memo

2. **Compatibilidade de APIs**
   - **Risco**: APIs do backend podem precisar de ajustes
   - **Mitigação**: Criar camada de adaptação no frontend

3. **Curva de Aprendizado**
   - **Risco**: Equipe pode não estar familiarizada com Next.js/TypeScript
   - **Mitigação**: Treinamento inicial e documentação detalhada

4. **Regressões de Funcionalidade**
   - **Risco**: Perder funcionalidades durante a migração
   - **Mitigação**: Testes abrangentes e checklist detalhado

5. **Tempo de Desenvolvimento**
   - **Risco**: Projeto pode levar mais tempo que o estimado
   - **Mitigação**: Priorizar funcionalidades core e fazer MVP primeiro

---

## ✅ Critérios de Sucesso

### Funcionais
- [ ] Todos os 6 dashboards funcionando perfeitamente
- [ ] Sistema de filtros de período operacional
- [ ] Sistema de alertas funcional
- [ ] Busca global implementada
- [ ] Comparação de períodos funcionando
- [ ] Exportação de relatórios (PDF/Excel)
- [ ] Tema dark/light mode
- [ ] Responsividade mobile

### Técnicos
- [ ] Cobertura de testes > 80%
- [ ] Performance score (Lighthouse) > 90
- [ ] Acessibilidade score (Lighthouse) > 90
- [ ] Bundle size otimizado
- [ ] Tempo de carregamento < 3s
- [ ] Zero erros TypeScript

### Negócio
- [ ] Paridade completa de funcionalidades
- [ ] Mesma ou melhor UX que o sistema atual
- [ ] Documentação completa
- [ ] Transição sem downtime
- [ ] Equipe treinada

---

## 📚 Recursos e Referências

### Documentação Oficial
- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

### Tutoriais e Guias
- [Next.js 14 App Router Tutorial](https://nextjs.org/learn)
- [TypeScript with React](https://react-typescript-cheatsheet.netlify.app/)
- [TanStack Query Guide](https://tanstack.com/query/latest/docs/react/overview)

### Ferramentas
- [Shadcn/ui Components](https://ui.shadcn.com/)
- [Radix UI](https://www.radix-ui.com/)
- [Recharts Examples](https://recharts.org/en-US/examples)

---

## 🤝 Equipe e Responsabilidades

### Papéis Recomendados

1. **Tech Lead**: Arquitetura e decisões técnicas
2. **Frontend Developers (2-3)**: Implementação de componentes e dashboards
3. **Backend Developer**: Ajustes na API se necessário
4. **QA Engineer**: Testes e validação
5. **DevOps**: Deploy e infraestrutura

---

## 📝 Notas Importantes

1. **Backend permanece inalterado**: A API FastAPI continuará funcionando sem modificações significativas
2. **Migração não-destrutiva**: O sistema atual continua funcionando durante todo o processo
3. **Prioridade em paridade de funcionalidades**: Primeiro replicar, depois melhorar
4. **Documentação contínua**: Cada fase deve ser documentada
5. **Code Review obrigatório**: Todas as mudanças devem passar por revisão

---

## 🔗 Links para as Fases

- [📋 Fase 1: Preparação e Setup Inicial](./MIGRATION_PHASE_1.md)
- [⚙️ Fase 2: Infraestrutura e Configurações](./MIGRATION_PHASE_2.md)
- [🎨 Fase 3: Componentes Base e Design System](./MIGRATION_PHASE_3.md)
- [📊 Fase 4: Dashboards - Parte 1](./MIGRATION_PHASE_4.md)
- [📈 Fase 5: Dashboards - Parte 2](./MIGRATION_PHASE_5.md)
- [🚀 Fase 6: Funcionalidades Avançadas](./MIGRATION_PHASE_6.md)
- [🧪 Fase 7: Integração e Testes](./MIGRATION_PHASE_7.md)
- [🌐 Fase 8: Deploy e Otimização](./MIGRATION_PHASE_8.md)

---

**Última atualização**: Janeiro 2026  
**Versão**: 1.0.0  
**Status**: 📋 Em Planejamento
