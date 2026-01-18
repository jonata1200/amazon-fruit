# 🍎 Amazon Fruit - Dashboard de Gestão Empresarial

> Sistema completo de dashboards para gestão de negócios, construído com Next.js 16, React 19 e TypeScript 5. Plataforma moderna com PWA, analytics e monitoramento de erros integrado.

[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue.svg)](https://www.typescriptlang.org/)
[![Next.js](https://img.shields.io/badge/Next.js-16.1-black.svg)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19.2-61dafb.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📖 Sobre o Projeto

Amazon Fruit é uma aplicação web moderna e completa para gestão empresarial, oferecendo dashboards interativos e em tempo real para análise estratégica de negócios. A plataforma foi desenvolvida com foco em performance, acessibilidade e experiência do usuário.

### Objetivo

Fornecer uma solução integrada de análise de dados empresariais, permitindo que gestores tomem decisões baseadas em informações precisas e atualizadas através de uma interface intuitiva e responsiva.

### Dashboards Disponíveis

- 📊 **Dashboard Geral** - Visão geral do negócio com KPIs principais
- 💰 **Dashboard de Finanças** - Análise detalhada de receitas, despesas e fluxo de caixa
- 📦 **Dashboard de Estoque** - Controle de produtos, alertas de baixo estoque e movimentações
- 👥 **Dashboard de Público-Alvo** - Segmentação demográfica e análise de comportamento
- 🏭 **Dashboard de Fornecedores** - Ranking, avaliação de performance e histórico
- 👔 **Dashboard de RH** - Headcount, custos operacionais e gestão de contratações

## 🖼️ Demonstração

> 💡 **Nota:** Adicione suas screenshots na pasta `public/images/` e atualize os caminhos abaixo.

### 📊 Dashboard Geral

Visão geral do negócio com KPIs principais e evolução financeira em tempo real.

![Dashboard Geral](./public/images/dashboard-geral.png)

### 💰 Dashboard de Finanças

Análise detalhada de receitas, despesas e fluxo de caixa.

![Dashboard de Finanças](./public/images/dashboard-financas.png)

### 📦 Dashboard de Estoque

Controle de produtos, alertas de baixo estoque e movimentações.

![Dashboard de Estoque](./public/images/dashboard-estoque.png)

### 👥 Dashboard de Público-Alvo

Segmentação demográfica e análise de comportamento.

![Dashboard de Público-Alvo](./public/images/dashboard-publico-alvo.png)

### 🏭 Dashboard de Fornecedores

Ranking, avaliação de performance e histórico de fornecedores.

![Dashboard de Fornecedores](./public/images/dashboard-fornecedores.png)

### 👔 Dashboard de Recursos Humanos

Headcount, custos operacionais e gestão de contratações.

![Dashboard de Recursos Humanos](./public/images/dashboard-recursos-humanos.png)

### 🎨 Recursos Visuais Adicionais

![Tema Escuro](./public/images/tema-escuro.png)


## ✨ Funcionalidades Principais

### 📊 Dashboards Especializados

- **Dashboard Geral** - KPIs principais e evolução financeira em tempo real
- **Dashboard de Finanças** - Análise detalhada de receitas, despesas e fluxo de caixa
- **Dashboard de Estoque** - Controle de produtos, alertas de baixo estoque e movimentações
- **Dashboard de Público-Alvo** - Segmentação demográfica e análise de comportamento
- **Dashboard de Fornecedores** - Ranking, avaliação de performance e histórico
- **Dashboard de RH** - Headcount, custos operacionais e gestão de contratações

### 🚀 Funcionalidades Avançadas

- 🔍 **Busca Global** - Pesquisa rápida em todos os dashboards (atalho: `Ctrl+K`)
- 🔔 **Sistema de Alertas** - Notificações em tempo real para eventos importantes
- 📤 **Exportação de Dados** - Relatórios em PDF, Excel e CSV
- ⌨️ **Atalhos de Teclado** - Navegação rápida e eficiente com ajuda integrada
- 🎨 **Temas Personalizados** - Modo claro e escuro com preferências salvas no localStorage
- 📱 **Design Responsivo** - Experiência otimizada para mobile e desktop
- 📱 **Progressive Web App (PWA)** - Funcionalidade offline e instalação como app nativo
- 📊 **Gráficos Interativos** - Visualizações dinâmicas com Recharts
- 🎯 **Analytics Integrado** - Rastreamento de eventos e métricas de uso
- 🛡️ **Tratamento de Erros** - Error boundaries e monitoramento com Sentry
- ♿ **Acessibilidade** - Conforme WCAG com suporte a leitores de tela
- 🚀 **Performance Otimizada** - Lazy loading, code splitting e cache inteligente

## 🚀 Início Rápido

### Pré-requisitos

- Node.js 20.x ou superior
- npm 10.x ou superior

### Instalação

1. **Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/amazon-fruit.git
cd amazon-fruit
```

2. **Instale as dependências:**

```bash
npm install
```

3. **Configure as variáveis de ambiente:**

```bash
cp .env.example .env.local
```

Edite `.env.local` com suas configurações:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=30000

# App Configuration
NEXT_PUBLIC_APP_NAME=Amazon Fruit
NEXT_PUBLIC_APP_VERSION=0.1.0
```

4. **Inicie o servidor de desenvolvimento:**

```bash
npm run dev
```

Acesse [http://localhost:3000](http://localhost:3000) no seu navegador.

## 📚 Scripts Disponíveis

### Desenvolvimento

| Script | Descrição |
|--------|-----------|
| `npm run dev` | Inicia servidor de desenvolvimento |
| `npm run build` | Compila para produção |
| `npm start` | Inicia servidor de produção |
| `npm run analyze` | Analisa o tamanho do bundle |

### Qualidade de Código

| Script | Descrição |
|--------|-----------|
| `npm run lint` | Executa ESLint |
| `npm run lint:fix` | Corrige problemas do ESLint automaticamente |
| `npm run format` | Formata código com Prettier |
| `npm run format:check` | Verifica formatação do código |
| `npm run type-check` | Verifica tipos TypeScript |

### Testes

| Script | Descrição |
|--------|-----------|
| `npm test` | Executa todos os testes unitários |
| `npm run test:watch` | Executa testes em modo watch |
| `npm run test:coverage` | Executa testes com cobertura |
| `npm run test:integration` | Executa testes de integração |
| `npm run test:integration:watch` | Executa testes de integração em modo watch |
| `npm run test:e2e` | Executa testes end-to-end com Playwright |
| `npm run test:e2e:ui` | Executa testes E2E com interface gráfica |
| `npm run test:e2e:headed` | Executa testes E2E em modo headed (com browser visível) |
| `npm run test:e2e:debug` | Executa testes E2E em modo debug |

### Storybook

| Script | Descrição |
|--------|-----------|
| `npm run storybook` | Inicia Storybook na porta 6006 |
| `npm run build-storybook` | Compila Storybook para produção |

## 🛠️ Tecnologias

### Stack Principal

- **[Next.js 16](https://nextjs.org/)** - Framework React com App Router e Turbopack
- **[React 19](https://react.dev/)** - Biblioteca UI com Server Components
- **[TypeScript 5](https://www.typescriptlang.org/)** - Tipagem estática

### Bibliotecas Principais

- **[Zustand](https://zustand-demo.pmnd.rs/)** - Gerenciamento de estado global
- **[TanStack Query](https://tanstack.com/query)** - Data fetching e caching
- **[Tailwind CSS v4](https://tailwindcss.com/)** - Framework CSS utility-first
- **[Recharts](https://recharts.org/)** - Biblioteca de gráficos interativos
- **[Lucide React](https://lucide.dev/)** - Ícones SVG
- **[Sonner](https://sonner.emilkowal.ski/)** - Toast notifications

### Bibliotecas de UI e Interação

- **[Framer Motion](https://www.framer.com/motion/)** - Animações fluidas
- **[React Hook Form](https://react-hook-form.com/)** - Gerenciamento de formulários
- **[Zod](https://zod.dev/)** - Validação de esquemas TypeScript-first
- **[date-fns](https://date-fns.org/)** - Manipulação de datas
- **[Axios](https://axios-http.com/)** - Cliente HTTP

### Ferramentas de Desenvolvimento

- **[Jest](https://jestjs.org/)** - Framework de testes unitários
- **[Testing Library](https://testing-library.com/)** - Testes de componentes React
- **[Playwright](https://playwright.dev/)** - Testes end-to-end
- **[ESLint](https://eslint.org/)** - Linter com configuração Next.js
- **[Prettier](https://prettier.io/)** - Formatador de código
- **[Husky](https://typicode.github.io/husky/)** - Git hooks
- **[lint-staged](https://github.com/lint-staged/lint-staged)** - Lint em arquivos staged

### Ferramentas de Produção

- **[Sentry](https://sentry.io/)** - Monitoramento de erros e performance
- **[Next PWA](https://github.com/shadowwalker/next-pwa)** - Suporte a Progressive Web App
- **[Storybook](https://storybook.js.org/)** - Documentação e testes visuais de componentes
- **[Bundle Analyzer](https://github.com/vercel/next.js/tree/canary/packages/next-bundle-analyzer)** - Análise de bundle

## 🧪 Testes

O projeto possui uma suíte completa de testes para garantir qualidade e confiabilidade do código.

### Estrutura de Testes

```
tests/
├── unit/              # Testes unitários de componentes e funções
├── integration/       # Testes de integração entre componentes
├── e2e/              # Testes end-to-end com Playwright
├── fixtures/         # Dados de teste e mocks
├── helpers/          # Utilitários para testes
└── templates/        # Templates para criar novos testes
```

### Executando Testes

```bash
# Todos os testes unitários
npm test

# Testes em modo watch (desenvolvimento)
npm run test:watch

# Testes com cobertura de código
npm run test:coverage

# Apenas testes de integração
npm run test:integration

# Testes end-to-end
npm run test:e2e

# Testes E2E com interface gráfica
npm run test:e2e:ui
```

### Tipos de Testes

- **Testes Unitários** - Testam componentes e funções isoladamente
- **Testes de Integração** - Testam interações entre múltiplos componentes
- **Testes E2E** - Testam fluxos completos do usuário com Playwright

### Cobertura de Testes

O projeto utiliza Jest para cobertura de código. Execute `npm run test:coverage` para gerar relatórios detalhados.

## 🚀 Deploy

### Vercel (Recomendado)

O projeto está otimizado para deploy na Vercel, plataforma oficial do Next.js:

1. **Faça push do código para o GitHub**
2. **Conecte o repositório na [Vercel](https://vercel.com)**
3. **Configure as variáveis de ambiente** no painel da Vercel:
   - `NEXT_PUBLIC_API_URL`
   - `NEXT_PUBLIC_APP_NAME`
   - `NEXT_PUBLIC_APP_VERSION`
4. **Deploy automático** a cada push para a branch principal!

### Docker

Para deploy com Docker:

```bash
# Build da imagem
docker build -t amazon-fruit .

# Executar container
docker run -p 3000:3000 amazon-fruit

# Ou com Docker Compose
docker-compose up -d
```

O projeto inclui `Dockerfile` e `docker-compose.yml` configurados e prontos para uso.

### Outras Plataformas

O projeto é compatível com várias plataformas de deploy:

- **Netlify** - Compatível com SSG/SSR do Next.js
- **Railway** - Deploy simplificado com Docker
- **AWS Amplify** - Deploy serverless
- **Azure Static Web Apps** - Hosting estático e serverless
- **Google Cloud Run** - Containers serverless

## 📁 Estrutura do Projeto

```
amazon-fruit/
├── src/
│   ├── app/                          # App Router (Next.js 16)
│   │   ├── (dashboards)/             # Rotas agrupadas dos dashboards
│   │   │   ├── geral/                # Dashboard geral
│   │   │   ├── financas/             # Dashboard de finanças
│   │   │   ├── estoque/              # Dashboard de estoque
│   │   │   ├── publico-alvo/         # Dashboard de público-alvo
│   │   │   ├── fornecedores/         # Dashboard de fornecedores
│   │   │   └── recursos-humanos/     # Dashboard de RH
│   │   ├── api/                      # API Routes
│   │   ├── layout.tsx                # Layout raiz
│   │   ├── page.tsx                  # Página inicial
│   │   └── error.tsx                 # Página de erro
│   ├── components/                   # Componentes React
│   │   ├── charts/                   # Componentes de gráficos (Recharts)
│   │   ├── dashboards/               # Componentes específicos de dashboards
│   │   ├── features/                 # Features complexas
│   │   │   ├── alerts/               # Sistema de alertas
│   │   │   ├── export/               # Exportação de dados
│   │   │   ├── keyboard/             # Atalhos de teclado
│   │   │   └── search/               # Busca global
│   │   ├── layouts/                  # Layouts (header, sidebar, footer)
│   │   ├── onboarding/               # Componentes de onboarding
│   │   └── ui/                       # Componentes UI base (shadcn/ui)
│   ├── lib/                          # Bibliotecas e utilidades
│   │   ├── analytics/                # Rastreamento de eventos
│   │   ├── api/                      # Cliente API e serviços
│   │   ├── constants/                # Constantes do projeto
│   │   ├── hooks/                    # Hooks customizados React
│   │   ├── providers/                # Context providers (Query, Theme)
│   │   ├── utils/                    # Funções utilitárias
│   │   └── validation/               # Schemas de validação (Zod)
│   ├── store/                        # Zustand stores (estado global)
│   ├── stories/                      # Componentes para Storybook
│   ├── styles/                       # Estilos globais e tokens
│   └── types/                        # Definições TypeScript
├── public/                           # Assets estáticos
│   ├── images/                       # Screenshots e imagens
│   ├── icons/                        # Ícones PWA
│   └── manifest.json                 # Manifest PWA
├── tests/                            # Testes
│   ├── e2e/                          # Testes end-to-end (Playwright)
│   ├── fixtures/                     # Dados de teste
│   ├── helpers/                      # Utilitários de teste
│   ├── integration/                  # Testes de integração
│   ├── templates/                    # Templates de teste
│   └── unit/                         # Testes unitários
├── .storybook/                       # Configuração do Storybook
├── coverage/                         # Relatórios de cobertura (gerado)
└── [config files]                    # Arquivos de configuração
```

### Padrões de Código

O projeto segue padrões rigorosos de qualidade:

- ✅ **TypeScript strict mode** - Tipagem forte e segura
- ✅ **ESLint** - Linter configurado com regras do Next.js
- ✅ **Prettier** - Formatação automática de código
- ✅ **Husky + lint-staged** - Hooks Git para garantir qualidade
- ✅ **Conventional Commits** - Padrão de mensagens de commit
- ✅ **Testes obrigatórios** - Novas features devem incluir testes
- ✅ **Acessibilidade** - Componentes acessíveis (WCAG)
- ✅ **Performance** - Otimizações de bundle e lazy loading

## 🔧 Configuração Avançada

### Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para configuração. Crie um arquivo `.env.local` baseado no `.env.example`:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=30000

# App Configuration
NEXT_PUBLIC_APP_NAME=Amazon Fruit
NEXT_PUBLIC_APP_VERSION=0.1.0
```

### Storybook

O projeto inclui Storybook para documentação e testes visuais de componentes:

```bash
# Iniciar Storybook
npm run storybook

# Build do Storybook
npm run build-storybook
```

Acesse `http://localhost:6006` para visualizar os componentes documentados.

### PWA (Progressive Web App)

O projeto está configurado como PWA, permitindo:
- Instalação como app nativo
- Funcionalidade offline
- Notificações push (quando configurado)
- Cache inteligente de assets

### Monitoramento

O projeto inclui integração com Sentry para:
- Monitoramento de erros em produção
- Rastreamento de performance
- Analytics de uso

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Checklist para Contribuições

- [ ] Código segue os padrões do projeto (ESLint, Prettier)
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada (se necessário)
- [ ] Tipo de commit segue o padrão Conventional Commits
- [ ] Build passa sem erros

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**Jonata Jesus**

- GitHub: [@jonata1200](https://github.com/jonata1200)

## 🙏 Agradecimentos

- Comunidade Next.js pelo excelente framework
- Todos os mantenedores das bibliotecas open-source utilizadas
- Contribuidores e revisores de código

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!
