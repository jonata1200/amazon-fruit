# 🍎 Amazon Fruit - Dashboard de Gestão

> Sistema completo de dashboards para gestão de negócios, construído com Next.js 16, React 19 e TypeScript 5.

[![CI](https://github.com/seu-usuario/amazon-fruit/actions/workflows/ci.yml/badge.svg)](https://github.com/seu-usuario/amazon-fruit/actions/workflows/ci.yml)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)
[![Next.js](https://img.shields.io/badge/Next.js-16-black.svg)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19-61dafb.svg)](https://reactjs.org/)

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Testes](#testes)
- [Deploy](#deploy)
- [Documentação](#documentação)
- [Contribuição](#contribuição)

## 📖 Sobre o Projeto

Amazon Fruit é uma aplicação web moderna para gestão empresarial, oferecendo dashboards interativos para análise de:

- 📊 Visão geral do negócio
- 💰 Finanças e fluxo de caixa
- 📦 Controle de estoque
- 👥 Análise de público-alvo
- 🏭 Gestão de fornecedores
- 👔 Recursos humanos

## ✨ Funcionalidades

### Dashboards

- ✅ **Dashboard Geral**: KPIs principais e evolução financeira
- ✅ **Dashboard de Finanças**: Análise detalhada de receitas e despesas
- ✅ **Dashboard de Estoque**: Controle de produtos e alertas de baixo estoque
- ✅ **Dashboard de Público-Alvo**: Segmentação e análise demográfica
- ✅ **Dashboard de Fornecedores**: Ranking e avaliação de fornecedores
- ✅ **Dashboard de RH**: Headcount, custos e contratações

### Funcionalidades Avançadas

- 🔍 **Busca Global**: Pesquisa rápida em todos os dashboards (Ctrl+K)
- 🔔 **Sistema de Alertas**: Notificações em tempo real
- 📤 **Exportação**: Relatórios em PDF, Excel e CSV
- ⌨️ **Atalhos de Teclado**: Navegação rápida
- 🎨 **Temas**: Modo claro e escuro
- 📱 **Responsivo**: Otimizado para mobile e desktop

## 🚀 Tecnologias

### Core

- **[Next.js 16](https://nextjs.org/)** - Framework React com App Router e Turbopack
- **[React 19](https://react.dev/)** - Biblioteca UI com Server Components
- **[TypeScript 5](https://www.typescriptlang.org/)** - Tipagem estática

### Estado e Dados

- **[Zustand](https://zustand-demo.pmnd.rs/)** - Gerenciamento de estado global
- **[TanStack Query](https://tanstack.com/query)** - Data fetching e caching
- **[Axios](https://axios-http.com/)** - Cliente HTTP

### UI e Estilização

- **[Tailwind CSS v4](https://tailwindcss.com/)** - Framework CSS utility-first
- **[Recharts](https://recharts.org/)** - Biblioteca de gráficos
- **[Lucide React](https://lucide.dev/)** - Ícones
- **[Class Variance Authority](https://cva.style/)** - Variantes de componentes
- **[Sonner](https://sonner.emilkowal.ski/)** - Toast notifications

### Qualidade e Testes

- **[Jest](https://jestjs.io/)** - Framework de testes
- **[Testing Library](https://testing-library.com/)** - Testes de componentes
- **[ESLint](https://eslint.org/)** - Linter
- **[Prettier](https://prettier.io/)** - Formatador de código

## 📦 Pré-requisitos

- Node.js 20.x ou superior
- npm 10.x ou superior

## 🔧 Instalação

1. Clone o repositório:

\`\`\`bash
git clone https://github.com/seu-usuario/amazon-fruit.git
cd amazon-fruit
\`\`\`

2. Instale as dependências:

\`\`\`bash
npm install
\`\`\`

3. Configure as variáveis de ambiente:

\`\`\`bash
cp .env.example .env.local
\`\`\`

Edite `.env.local` com suas configurações:

\`\`\`env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Amazon Fruit
\`\`\`

## 🎮 Uso

### Desenvolvimento

\`\`\`bash
npm run dev
\`\`\`

Acesse [http://localhost:3000](http://localhost:3000)

### Produção

\`\`\`bash
npm run build
npm start
\`\`\`

### Scripts Disponíveis

| Script | Descrição |
|--------|-----------|
| `npm run dev` | Inicia servidor de desenvolvimento |
| `npm run build` | Compila para produção |
| `npm start` | Inicia servidor de produção |
| `npm test` | Executa testes |
| `npm run lint` | Executa linter |
| `npm run type-check` | Verifica tipos TypeScript |
| `npm run format` | Formata código com Prettier |

## 🧪 Testes

Execute os testes:

\`\`\`bash
npm test
\`\`\`

Testes com cobertura:

\`\`\`bash
npm test -- --coverage
\`\`\`

Testes em watch mode:

\`\`\`bash
npm test -- --watch
\`\`\`

### Cobertura

- ✅ 58 testes implementados
- ✅ 100% taxa de sucesso
- ✅ Componentes UI, Hooks, Features e Dashboards

## 🐳 Deploy

### Docker

Build da imagem:

\`\`\`bash
docker build -t amazon-fruit .
\`\`\`

Executar container:

\`\`\`bash
docker run -p 3000:3000 amazon-fruit
\`\`\`

Com Docker Compose:

\`\`\`bash
docker-compose up -d
\`\`\`

### Vercel (Recomendado)

1. Faça push para o GitHub
2. Conecte seu repositório no [Vercel](https://vercel.com)
3. Configure as variáveis de ambiente
4. Deploy automático!

### Outras Plataformas

- **Netlify**: Compatível com SSG/SSR
- **Railway**: Deploy com Docker
- **AWS/GCP/Azure**: Deploy com containers

## 📚 Documentação

Documentação completa disponível em:

- [📖 Visão Geral da Migração](docs/MIGRATION_PLAN_OVERVIEW.md)
- [🚀 Quick Start](docs/MIGRATION_QUICK_START.md)
- [📋 Sumário Executivo](docs/MIGRATION_EXECUTIVE_SUMMARY.md)
- [📝 Changelog](CHANGELOG.md)

### Fases de Implementação

1. ✅ [Fase 1: Preparação e Setup](docs/MIGRATION_PHASE_1.md)
2. ✅ [Fase 2: Infraestrutura](docs/MIGRATION_PHASE_2.md)
3. ✅ [Fase 3: Componentes Base](docs/MIGRATION_PHASE_3.md)
4. ✅ [Fase 4: Dashboards - Parte 1](docs/MIGRATION_PHASE_4.md)
5. ✅ [Fase 5: Dashboards - Parte 2](docs/MIGRATION_PHASE_5.md)
6. ✅ [Fase 6: Funcionalidades Avançadas](docs/MIGRATION_PHASE_6.md)
7. ✅ [Fase 7: Integração e Testes](docs/MIGRATION_PHASE_7.md)
8. ✅ [Fase 8: Otimização e Deploy](docs/MIGRATION_PHASE_8.md)

## 🎯 Estrutura do Projeto

\`\`\`
amazon-fruit/
├── src/
│   ├── app/                  # App Router (Next.js 16)
│   │   ├── (dashboards)/     # Rotas dos dashboards
│   │   ├── layout.tsx        # Layout raiz
│   │   └── page.tsx          # Página inicial
│   ├── components/           # Componentes React
│   │   ├── charts/           # Componentes de gráficos
│   │   ├── dashboards/       # Componentes de dashboards
│   │   ├── features/         # Features (alertas, busca, etc)
│   │   ├── layouts/          # Layouts (header, sidebar, footer)
│   │   └── ui/               # Componentes UI base
│   ├── lib/                  # Bibliotecas e utilidades
│   │   ├── api/              # Cliente API e serviços
│   │   ├── hooks/            # Hooks customizados
│   │   ├── providers/        # Providers (Query, Theme)
│   │   └── utils/            # Funções utilitárias
│   ├── store/                # Zustand stores
│   ├── styles/               # Estilos globais
│   └── types/                # Definições TypeScript
├── tests/                    # Testes e helpers
├── public/                   # Assets estáticos
└── docs/                     # Documentação
\`\`\`

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código

- ✅ TypeScript strict mode
- ✅ ESLint configurado
- ✅ Prettier para formatação
- ✅ Testes obrigatórios para novas features

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Equipe de Desenvolvimento** - [GitHub](https://github.com/seu-usuario)

## 🙏 Agradecimentos

- Next.js Team pelo framework incrível
- Vercel pela plataforma de deploy
- Comunidade open source

---

<div align="center">
  <strong>Feito com ❤️ usando Next.js 16 e React 19</strong>
</div>
