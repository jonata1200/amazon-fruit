# 🤝 Guia de Contribuição

## Como Adicionar Novos Design Tokens

### 1. Adicionar Token de Cor

Edite `src/lib/design-tokens/colors.ts`:

```typescript
export const colors = {
  // ... cores existentes
  newColor: {
    50: '#...',
    // ... escala completa
    950: '#...',
  },
} as const;
```

### 2. Adicionar Token de Espaçamento

Edite `src/lib/design-tokens/spacing.ts`:

```typescript
export const spacing = {
  // ... espaçamentos existentes
  newSize: '2.5rem', // 40px
} as const;
```

### 3. Atualizar Types

Edite `src/lib/design-tokens/types.ts` para incluir novos tipos.

### 4. Atualizar Tailwind Config

Adicione o token em `tailwind.config.ts` se necessário.

## Como Criar Novos Componentes

### 1. Estrutura Base

```tsx
/**
 * Componente [Nome] - [Descrição]
 * [Descrição detalhada]
 */

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const [nome]Variants = cva(
  'base-classes',
  {
    variants: {
      // variantes
    },
    defaultVariants: {
      // defaults
    },
  }
);

export interface [Nome]Props
  extends React.HTMLAttributes<HTMLElement>,
    VariantProps<typeof [nome]Variants> {}

const [Nome] = React.forwardRef<HTMLElement, [Nome]Props>(
  ({ className, ...props }, ref) => {
    return (
      <element
        ref={ref}
        className={cn([nome]Variants(), className)}
        {...props}
      />
    );
  }
);
[Nome].displayName = '[Nome]';

export { [Nome], [nome]Variants };
```

### 2. Checklist de Componente

- [ ] Usa `forwardRef` para refs
- [ ] Usa `cva` para variantes
- [ ] Usa `cn()` para classes
- [ ] Type-safe com TypeScript
- [ ] Acessível (ARIA, keyboard)
- [ ] Suporta dark mode
- [ ] Documentado com JSDoc
- [ ] Exportado no index

### 3. Adicionar ao Index

```typescript
// src/components/ui/index.ts
export { [Nome] } from './[nome]';
```

## Processo de Revisão

1. **Criar branch** para a feature
2. **Implementar** seguindo padrões
3. **Testar** em diferentes contextos
4. **Documentar** mudanças
5. **Criar PR** com descrição clara

## Convenções de Código

### Nomenclatura
- **Componentes**: PascalCase (`Button`, `Card`)
- **Arquivos**: kebab-case (`button.tsx`, `card.tsx`)
- **Variáveis**: camelCase (`isActive`, `handleClick`)
- **Constantes**: UPPER_SNAKE_CASE (`MAX_SIZE`)

### Estrutura de Arquivo
```tsx
// 1. Imports
import ...

// 2. Types/Interfaces
export interface ...

// 3. Variants (se usar cva)
const variants = cva(...)

// 4. Component
const Component = ...

// 5. Exports
export { Component };
```

### Comentários
- Use JSDoc para funções públicas
- Comente decisões importantes
- Mantenha comentários atualizados

## Testes

### Unit Tests
```typescript
describe('Button', () => {
  it('renders correctly', () => {
    // teste
  });
});
```

### Acessibilidade
- Teste com leitores de tela
- Teste navegação por teclado
- Verifique contraste de cores

## Documentação

### Atualizar Docs
1. Adicione exemplos em `docs/components/[nome].md`
2. Atualize `docs/README.md` se necessário
3. Adicione ao changelog se for breaking change

## Checklist de Contribuição

Antes de submeter:
- [ ] Código segue convenções
- [ ] TypeScript sem erros
- [ ] Testes passando
- [ ] Documentação atualizada
- [ ] Acessibilidade verificada
- [ ] Dark mode testado
- [ ] Responsivo testado

## Dúvidas?

Abra uma issue ou entre em contato com a equipe de design system.
