# 📋 Fase 1: Preparação e Setup Inicial

**Duração Estimada**: 2-3 dias  
**Complexidade**: Baixa  
**Dependências**: Nenhuma

---

## 🎯 Objetivos desta Fase

1. Configurar o ambiente de desenvolvimento Next.js
2. Definir e criar a estrutura de pastas do projeto
3. Configurar TypeScript com as melhores práticas
4. Configurar ferramentas de qualidade de código (ESLint, Prettier)
5. Instalar e configurar bibliotecas essenciais
6. Criar projeto base funcional

---

## 📋 Checklist de Ações

### 1. Setup Inicial do Projeto

- [x] **1.1** Criar novo diretório para o projeto Next.js
  ```bash
  mkdir amazon-fruit
  cd amazon-fruit
  ```

- [x] **1.2** Inicializar projeto Next.js com TypeScript
  ```bash
  npx create-next-app@latest . --typescript --tailwind --app --use-npm
  ```
  - Responder às perguntas do CLI:
    - TypeScript: **Yes**
    - ESLint: **Yes**
    - Tailwind CSS: **Yes**
    - `src/` directory: **Yes**
    - App Router: **Yes**
    - Import alias: **Yes** (@/*)

- [x] **1.3** Verificar instalação
  ```bash
  npm run dev
  ```
  - Acessar http://localhost:3000
  - Verificar se a página inicial do Next.js carrega

---

### 2. Estrutura de Pastas

- [x] **2.1** Criar estrutura de diretórios base
  ```bash
  # No diretório raiz do projeto Next.js
  mkdir -p src/components/{ui,layouts,dashboards,charts,features}
  mkdir -p src/lib/{api,hooks,utils,constants}
  mkdir -p src/store/slices
  mkdir -p src/types
  mkdir -p src/styles
  mkdir -p tests/{unit,integration,e2e}
  mkdir -p public/{images,icons}
  ```

- [x] **2.2** Criar arquivos base vazios
  ```bash
  # Types
  touch src/types/api.ts
  touch src/types/dashboard.ts
  touch src/types/index.ts
  
  # Store
  touch src/store/index.ts
  
  # Lib
  touch src/lib/api/client.ts
  touch src/lib/constants/index.ts
  touch src/lib/utils/index.ts
  
  # Styles
  touch src/styles/theme.ts
  ```

- [x] **2.3** Criar arquivo README.md do projeto Next.js
  ```bash
  touch README.md
  ```

---

### 3. Configuração do TypeScript

- [x] **3.1** Atualizar `tsconfig.json` com configurações otimizadas
  ```json
  {
    "compilerOptions": {
      "target": "ES2020",
      "lib": ["dom", "dom.iterable", "esnext"],
      "allowJs": true,
      "skipLibCheck": true,
      "strict": true,
      "noEmit": true,
      "esModuleInterop": true,
      "module": "esnext",
      "moduleResolution": "bundler",
      "resolveJsonModule": true,
      "isolatedModules": true,
      "jsx": "preserve",
      "incremental": true,
      "plugins": [
        {
          "name": "next"
        }
      ],
      "paths": {
        "@/*": ["./src/*"],
        "@/components/*": ["./src/components/*"],
        "@/lib/*": ["./src/lib/*"],
        "@/types/*": ["./src/types/*"],
        "@/store/*": ["./src/store/*"],
        "@/styles/*": ["./src/styles/*"]
      },
      "strictNullChecks": true,
      "noUnusedLocals": true,
      "noUnusedParameters": true,
      "noImplicitReturns": true,
      "noFallthroughCasesInSwitch": true
    },
    "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
    "exclude": ["node_modules"]
  }
  ```

- [x] **3.2** Criar arquivo `next-env.d.ts` se não existir
  ```typescript
  /// <reference types="next" />
  /// <reference types="next/image-types/global" />
  ```

---

### 4. Configuração do ESLint

- [x] **4.1** Configurar ESLint
  > **Nota**: Next.js 16 usa `eslint.config.mjs` ao invés de `.eslintrc.json`. O arquivo já está configurado com as configurações do Next.js.

- [x] **4.2** Instalar plugins adicionais do ESLint
  ```bash
  npm install -D @typescript-eslint/eslint-plugin @typescript-eslint/parser
  ```

---

### 5. Configuração do Prettier

- [x] **5.1** Instalar Prettier e plugins
  ```bash
  npm install -D prettier eslint-config-prettier eslint-plugin-prettier
  ```

- [x] **5.2** Criar `.prettierrc`
  ```json
  {
    "semi": true,
    "trailingComma": "es5",
    "singleQuote": true,
    "printWidth": 100,
    "tabWidth": 2,
    "useTabs": false,
    "arrowParens": "always",
    "endOfLine": "lf"
  }
  ```

- [x] **5.3** Criar `.prettierignore`
  ```
  node_modules
  .next
  out
  dist
  build
  coverage
  *.min.js
  package-lock.json
  yarn.lock
  pnpm-lock.yaml
  ```

- [x] **5.4** Atualizar `.eslintrc.json` para integrar com Prettier
  ```json
  {
    "extends": [
      "next/core-web-vitals",
      "plugin:@typescript-eslint/recommended",
      "prettier"
    ]
  }
  ```

---

### 6. Instalação de Dependências Essenciais

- [x] **6.1** Instalar bibliotecas de UI e estilização
  ```bash
  npm install class-variance-authority clsx tailwind-merge
  npm install lucide-react
  ```

- [x] **6.2** Instalar bibliotecas para gerenciamento de dados
  ```bash
  npm install axios
  npm install @tanstack/react-query
  npm install zustand
  ```

- [x] **6.3** Instalar bibliotecas de gráficos
  ```bash
  npm install recharts
  # OU se preferir Plotly:
  # npm install react-plotly.js plotly.js
  # npm install -D @types/plotly.js
  ```

- [x] **6.4** Instalar bibliotecas utilitárias
  ```bash
  npm install date-fns
  npm install react-hook-form
  npm install zod
  ```

- [x] **6.5** Instalar bibliotecas de testes
  ```bash
  npm install -D jest @testing-library/react @testing-library/jest-dom
  npm install -D @testing-library/user-event
  npm install -D jest-environment-jsdom
  ```

---

### 7. Configuração de Scripts no package.json

- [x] **7.1** Adicionar scripts úteis ao `package.json`
  ```json
  {
    "scripts": {
      "dev": "next dev",
      "build": "next build",
      "start": "next start",
      "lint": "next lint",
      "lint:fix": "next lint --fix",
      "format": "prettier --write \"src/**/*.{js,jsx,ts,tsx,json,css,scss,md}\"",
      "format:check": "prettier --check \"src/**/*.{js,jsx,ts,tsx,json,css,scss,md}\"",
      "type-check": "tsc --noEmit",
      "test": "jest",
      "test:watch": "jest --watch",
      "test:coverage": "jest --coverage"
    }
  }
  ```

---

### 8. Configuração do Tailwind CSS

- [x] **8.1** Atualizar `tailwind.config.ts` com tema customizado
  ```typescript
  import type { Config } from 'tailwindcss'

  const config: Config = {
    darkMode: ['class'],
    content: [
      './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
      './src/components/**/*.{js,ts,jsx,tsx,mdx}',
      './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    ],
    theme: {
      extend: {
        colors: {
          border: 'hsl(var(--border))',
          input: 'hsl(var(--input))',
          ring: 'hsl(var(--ring))',
          background: 'hsl(var(--background))',
          foreground: 'hsl(var(--foreground))',
          primary: {
            DEFAULT: 'hsl(var(--primary))',
            foreground: 'hsl(var(--primary-foreground))',
          },
          secondary: {
            DEFAULT: 'hsl(var(--secondary))',
            foreground: 'hsl(var(--secondary-foreground))',
          },
          destructive: {
            DEFAULT: 'hsl(var(--destructive))',
            foreground: 'hsl(var(--destructive-foreground))',
          },
          muted: {
            DEFAULT: 'hsl(var(--muted))',
            foreground: 'hsl(var(--muted-foreground))',
          },
          accent: {
            DEFAULT: 'hsl(var(--accent))',
            foreground: 'hsl(var(--accent-foreground))',
          },
          popover: {
            DEFAULT: 'hsl(var(--popover))',
            foreground: 'hsl(var(--popover-foreground))',
          },
          card: {
            DEFAULT: 'hsl(var(--card))',
            foreground: 'hsl(var(--card-foreground))',
          },
        },
        borderRadius: {
          lg: 'var(--radius)',
          md: 'calc(var(--radius) - 2px)',
          sm: 'calc(var(--radius) - 4px)',
        },
      },
    },
    plugins: [require('tailwindcss-animate')],
  }
  export default config
  ```

- [x] **8.2** Instalar plugin de animações do Tailwind
  ```bash
  npm install tailwindcss-animate
  ```

- [x] **8.3** Atualizar `src/app/globals.css` com variáveis CSS
  ```css
  @tailwind base;
  @tailwind components;
  @tailwind utilities;

  @layer base {
    :root {
      --background: 0 0% 100%;
      --foreground: 222.2 84% 4.9%;
      --card: 0 0% 100%;
      --card-foreground: 222.2 84% 4.9%;
      --popover: 0 0% 100%;
      --popover-foreground: 222.2 84% 4.9%;
      --primary: 222.2 47.4% 11.2%;
      --primary-foreground: 210 40% 98%;
      --secondary: 210 40% 96.1%;
      --secondary-foreground: 222.2 47.4% 11.2%;
      --muted: 210 40% 96.1%;
      --muted-foreground: 215.4 16.3% 46.9%;
      --accent: 210 40% 96.1%;
      --accent-foreground: 222.2 47.4% 11.2%;
      --destructive: 0 84.2% 60.2%;
      --destructive-foreground: 210 40% 98%;
      --border: 214.3 31.8% 91.4%;
      --input: 214.3 31.8% 91.4%;
      --ring: 222.2 84% 4.9%;
      --radius: 0.5rem;
    }

    .dark {
      --background: 222.2 84% 4.9%;
      --foreground: 210 40% 98%;
      --card: 222.2 84% 4.9%;
      --card-foreground: 210 40% 98%;
      --popover: 222.2 84% 4.9%;
      --popover-foreground: 210 40% 98%;
      --primary: 210 40% 98%;
      --primary-foreground: 222.2 47.4% 11.2%;
      --secondary: 217.2 32.6% 17.5%;
      --secondary-foreground: 210 40% 98%;
      --muted: 217.2 32.6% 17.5%;
      --muted-foreground: 215 20.2% 65.1%;
      --accent: 217.2 32.6% 17.5%;
      --accent-foreground: 210 40% 98%;
      --destructive: 0 62.8% 30.6%;
      --destructive-foreground: 210 40% 98%;
      --border: 217.2 32.6% 17.5%;
      --input: 217.2 32.6% 17.5%;
      --ring: 212.7 26.8% 83.9%;
    }
  }

  @layer base {
    * {
      @apply border-border;
    }
    body {
      @apply bg-background text-foreground;
    }
  }
  ```

---

### 9. Configuração de Variáveis de Ambiente

- [x] **9.1** Criar arquivo `.env.local`
  ```env
  # API Configuration
  NEXT_PUBLIC_API_URL=http://localhost:8000
  NEXT_PUBLIC_API_TIMEOUT=30000
  
  # App Configuration
  NEXT_PUBLIC_APP_NAME=Amazon Fruit
  NEXT_PUBLIC_APP_VERSION=2.0.0
  
  # Feature Flags (para migração gradual)
  NEXT_PUBLIC_ENABLE_NEW_DASHBOARD=false
  ```

- [x] **9.2** Criar arquivo `.env.example`
  ```env
  # API Configuration
  NEXT_PUBLIC_API_URL=
  NEXT_PUBLIC_API_TIMEOUT=
  
  # App Configuration
  NEXT_PUBLIC_APP_NAME=
  NEXT_PUBLIC_APP_VERSION=
  ```

- [x] **9.3** Adicionar `.env.local` ao `.gitignore`
  ```
  # Verificar se já existe no .gitignore
  # Se não, adicionar:
  .env*.local
  ```

---

### 10. Configuração de Controle de Versão

- [x] **10.1** Verificar arquivo `.gitignore` (já vem com Next.js, mas verificar)
  ```
  # dependencies
  /node_modules
  /.pnp
  .pnp.js

  # testing
  /coverage

  # next.js
  /.next/
  /out/

  # production
  /build

  # misc
  .DS_Store
  *.pem

  # debug
  npm-debug.log*
  yarn-debug.log*
  yarn-error.log*

  # local env files
  .env*.local

  # vercel
  .vercel

  # typescript
  *.tsbuildinfo
  next-env.d.ts
  ```

---

### 11. Configuração do Jest para Testes

- [x] **11.1** Criar arquivo `jest.config.js`
  ```javascript
  const nextJest = require('next/jest')

  const createJestConfig = nextJest({
    // Provide the path to your Next.js app to load next.config.js and .env files in your test environment
    dir: './',
  })

  // Add any custom config to be passed to Jest
  const customJestConfig = {
    setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
    testEnvironment: 'jest-environment-jsdom',
    moduleNameMapper: {
      '^@/(.*)$': '<rootDir>/src/$1',
    },
    collectCoverageFrom: [
      'src/**/*.{js,jsx,ts,tsx}',
      '!src/**/*.d.ts',
      '!src/**/*.stories.{js,jsx,ts,tsx}',
      '!src/**/__tests__/**',
    ],
  }

  // createJestConfig is exported this way to ensure that next/jest can load the Next.js config which is async
  module.exports = createJestConfig(customJestConfig)
  ```

- [x] **11.2** Criar arquivo `jest.setup.js`
  ```javascript
  import '@testing-library/jest-dom'
  ```

---

### 12. Criação de Componentes Base de Teste

- [x] **12.1** Criar componente de teste em `src/components/ui/Button.tsx`
  ```typescript
  import React from 'react';

  interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'outline';
    children: React.ReactNode;
  }

  export const Button: React.FC<ButtonProps> = ({ 
    variant = 'primary', 
    children, 
    className = '',
    ...props 
  }) => {
    return (
      <button 
        className={`btn btn-${variant} ${className}`} 
        {...props}
      >
        {children}
      </button>
    );
  };
  ```

- [x] **12.2** Criar teste para o componente Button
  ```typescript
  // src/components/ui/Button.test.tsx
  import { render, screen } from '@testing-library/react';
  import { Button } from './Button';

  describe('Button', () => {
    it('renders button with text', () => {
      render(<Button>Click me</Button>);
      expect(screen.getByText('Click me')).toBeInTheDocument();
    });
  });
  ```

- [x] **12.3** Executar teste para verificar configuração
  ```bash
  npm test
  ```

---

### 13. Documentação Inicial

- [x] **13.1** Criar README.md básico do projeto Next.js
  ```markdown
  # Amazon Fruit - Next.js

  Sistema de análise de dados empresariais construído com React, Next.js e TypeScript.

  ## Tecnologias

  - Next.js 16
  - React 19
  - TypeScript 5
  - Tailwind CSS v4
  - Zustand (State Management)
  - TanStack Query (Data Fetching)
  - Recharts (Visualizações)

  ## Desenvolvimento

  \`\`\`bash
  npm install
  npm run dev
  \`\`\`

  ## Testes

  \`\`\`bash
  npm test
  \`\`\`

  ## Build

  \`\`\`bash
  npm run build
  npm start
  \`\`\`
  ```

- [x] **13.2** Criar arquivo CHANGELOG.md
  ```markdown
  # Changelog

  ## [Unreleased]

  ### Added
  - Setup inicial do projeto Next.js
  - Configuração de TypeScript, ESLint e Prettier
  - Estrutura de pastas base
  ```

---

### 14. Verificação Final

- [x] **14.1** Executar linting
  ```bash
  npm run lint
  ```

- [x] **14.2** Executar verificação de tipos
  ```bash
  npm run type-check
  ```

- [x] **14.3** Executar formatação
  ```bash
  npm run format
  ```

- [x] **14.4** Executar testes
  ```bash
  npm test
  ```

- [x] **14.5** Executar build de produção
  ```bash
  npm run build
  ```

- [x] **14.6** Verificar se servidor de desenvolvimento funciona
  ```bash
  npm run dev
  # Acessar http://localhost:3000
  ```

---

### 15. Documentação

- [x] **15.1** Atualizar documentação da migração
  - Marcar Fase 1 como concluída no `MIGRATION_PLAN_OVERVIEW.md`
  - Documentar quaisquer decisões técnicas importantes tomadas

---

## ✅ Critérios de Conclusão da Fase 1

A Fase 1 está completa quando:

- [x] Projeto Next.js criado e funcionando
- [x] TypeScript configurado corretamente sem erros
- [x] ESLint e Prettier funcionando
- [x] Estrutura de pastas criada
- [x] Todas as dependências essenciais instaladas
- [x] Testes configurados e executando
- [x] Build de produção executando sem erros
- [x] Variáveis de ambiente configuradas
- [x] Documentação inicial criada

---

## 📝 Notas e Observações

### Decisões Técnicas

1. **Escolha do Tailwind CSS**: Optamos por Tailwind CSS v4 devido à sua flexibilidade, performance e sistema moderno de temas
2. **Zustand vs Context API**: Zustand oferece melhor performance e Developer Experience
3. **Recharts vs Plotly**: Optamos por Recharts para melhor integração com React e performance
4. **Next.js 16 com Turbopack**: Utilizamos a versão mais recente com Turbopack para builds mais rápidos
5. **TypeScript Strict Mode**: Configurado com todas as opções de segurança ativadas para melhor type safety

### Problemas Encontrados e Soluções

1. **Tailwind CSS v4 Sintaxe**:
   - **Problema**: A sintaxe do Tailwind v4 é diferente da v3, causando erros no build com `@layer base`
   - **Solução**: Adaptamos o globals.css para usar `@theme inline` e definições de cores diretas

2. **Jest Types**:
   - **Problema**: Erros de TypeScript com tipos do Jest não reconhecidos
   - **Solução**: Instalamos `@types/jest` e adicionamos import do `@testing-library/jest-dom` nos testes

3. **Tailwind darkMode**:
   - **Problema**: Configuração do darkMode como array causava erro de tipo
   - **Solução**: Mudamos de `['class']` para `'class'`

### Configurações Implementadas

- ✅ Next.js 16.1.1 com App Router e Turbopack
- ✅ TypeScript 5 com strict mode completo
- ✅ ESLint + Prettier configurados
- ✅ Tailwind CSS v4 com tema customizado
- ✅ Jest + React Testing Library
- ✅ Zustand, TanStack Query, Axios instalados
- ✅ Recharts para visualizações
- ✅ Estrutura de pastas completa
- ✅ Variáveis de ambiente configuradas

### Próximos Passos

- Prosseguir para [Fase 2: Infraestrutura e Configurações](./MIGRATION_PHASE_2.md)

---

**Status**: ✅ Concluída  
**Responsável**: Equipe de Desenvolvimento  
**Data de Início**: 13/01/2026  
**Data de Conclusão**: 13/01/2026
