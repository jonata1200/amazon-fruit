# Amazon Fruit - Next.js

Sistema de análise de dados empresariais construído com React, Next.js e TypeScript.

## 🛠️ Tecnologias

- Next.js 14
- React 18
- TypeScript 5
- Tailwind CSS
- Zustand (State Management)
- TanStack Query (Data Fetching)
- Recharts (Visualizações)

## 🚀 Desenvolvimento

```bash
npm install
npm run dev
```

Abra [http://localhost:3000](http://localhost:3000) para ver o resultado.

## 🧪 Testes

```bash
# Executar testes
npm test

# Executar testes em modo watch
npm run test:watch

# Executar testes com cobertura
npm run test:coverage
```

## 📦 Build

```bash
npm run build
npm start
```

## 📝 Scripts Disponíveis

- `npm run dev` - Inicia o servidor de desenvolvimento
- `npm run build` - Cria o build de produção
- `npm run start` - Inicia o servidor de produção
- `npm run lint` - Executa o linter
- `npm run lint:fix` - Corrige problemas do linter automaticamente
- `npm run format` - Formata o código com Prettier
- `npm run format:check` - Verifica a formatação do código
- `npm run type-check` - Verifica os tipos TypeScript

## 📁 Estrutura do Projeto

```
amazon-fruit-nextjs/
├── src/
│   ├── app/              # App Router do Next.js
│   ├── components/       # Componentes React
│   │   ├── ui/          # Componentes de UI base
│   │   ├── layouts/     # Layouts
│   │   ├── dashboards/  # Componentes de dashboards
│   │   ├── charts/      # Componentes de gráficos
│   │   └── features/    # Features complexas
│   ├── lib/             # Bibliotecas e utilitários
│   │   ├── api/        # Cliente da API
│   │   ├── hooks/      # Custom hooks
│   │   ├── utils/      # Funções utilitárias
│   │   └── constants/  # Constantes
│   ├── store/          # Estado global
│   ├── types/          # Tipos TypeScript
│   └── styles/         # Estilos
├── tests/              # Testes
│   ├── unit/          # Testes unitários
│   ├── integration/   # Testes de integração
│   └── e2e/           # Testes end-to-end
└── public/            # Arquivos estáticos
```

## 📚 Documentação

Para mais informações sobre o projeto e plano de migração, consulte a [documentação](../amazon-fruit/docs/README_MIGRATION.md).

## 📄 Licença

MIT
