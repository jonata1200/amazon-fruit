# 🎨 Design System - Amazon Fruit

Este documento descreve o Design System do projeto Amazon Fruit, incluindo tokens de design, componentes e padrões de uso.

## 🎨 Design Tokens

### Cores

O sistema de cores está definido em `src/lib/design-tokens.ts` e segue uma escala de 50-950 para cada cor principal.

#### Cores Principais

- **Primary (Lilás)**: Cor principal da marca
  - 50: `#faf5ff` (mais claro)
  - 600: `#9333ea` (cor principal)
  - 950: `#3b0764` (mais escuro)

- **Secondary (Cinza)**: Cores neutras para textos e backgrounds
- **Success (Verde)**: Feedback positivo, sucesso
- **Warning (Amarelo)**: Avisos, atenção
- **Error (Vermelho)**: Erros, ações destrutivas
- **Info (Azul)**: Informações, links

### Espaçamento

Escala de espaçamento baseada em múltiplos de 4px:

- `xs`: 0.25rem (4px)
- `sm`: 0.5rem (8px)
- `md`: 1rem (16px)
- `lg`: 1.5rem (24px)
- `xl`: 2rem (32px)
- `2xl`: 3rem (48px)
- `3xl`: 4rem (64px)
- `4xl`: 6rem (96px)
- `5xl`: 8rem (128px)

### Tipografia

#### Fontes

- **Sans**: `var(--font-geist-sans)` - Fonte principal
- **Mono**: `var(--font-geist-mono)` - Código, dados

#### Tamanhos

- `xs`: 0.75rem (12px)
- `sm`: 0.875rem (14px)
- `base`: 1rem (16px)
- `lg`: 1.125rem (18px)
- `xl`: 1.25rem (20px)
- `2xl`: 1.5rem (24px)
- `3xl`: 1.875rem (30px)
- `4xl`: 2.25rem (36px)
- `5xl`: 3rem (48px)
- `6xl`: 3.75rem (60px)

#### Pesos

- `light`: 300
- `normal`: 400
- `medium`: 500
- `semibold`: 600
- `bold`: 700
- `extrabold`: 800

### Border Radius

- `none`: 0
- `sm`: 0.125rem (2px)
- `base`: 0.25rem (4px)
- `md`: 0.375rem (6px)
- `lg`: 0.5rem (8px)
- `xl`: 0.75rem (12px)
- `2xl`: 1rem (16px)
- `3xl`: 1.5rem (24px)
- `full`: 9999px

### Shadows

Escala de elevação para profundidade visual:

- `sm`: Sombra pequena
- `base`: Sombra padrão
- `md`: Sombra média
- `lg`: Sombra grande
- `xl`: Sombra extra grande
- `2xl`: Sombra máxima
- `inner`: Sombra interna
- `none`: Sem sombra

### Breakpoints

- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

## 🧩 Componentes

### Button

Variantes disponíveis:
- `default`: Botão primário
- `destructive`: Ações destrutivas
- `outline`: Botão com borda
- `secondary`: Botão secundário
- `ghost`: Botão sem background
- `link`: Estilo de link

Tamanhos:
- `default`: Altura padrão
- `sm`: Pequeno
- `lg`: Grande
- `icon`: Quadrado para ícones

### Card

Componente de container para conteúdo agrupado.

### Input

Tipos suportados:
- `text`: Texto padrão
- `email`: Email
- `password`: Senha
- `number`: Números
- `date`: Data
- `search`: Busca

### Dialog

Modal para conteúdo importante que requer atenção do usuário.

### Icon

Sistema de ícones baseado em Lucide React com tamanhos padronizados:
- `xs`: 12px
- `sm`: 16px
- `md`: 20px
- `lg`: 24px
- `xl`: 32px

## 📐 Princípios de Design

### Consistência

- Use os tokens de design definidos
- Siga os padrões estabelecidos
- Mantenha consistência visual

### Acessibilidade

- Contraste mínimo de 4.5:1 para texto
- Navegação por teclado
- Labels descritivos
- Estados claros

### Performance

- Componentes memoizados quando apropriado
- Lazy loading para componentes pesados
- Otimização de re-renders

## 🔗 Recursos

- [Design Tokens](./src/lib/design-tokens.ts)
- [Componentes UI](./src/components/ui/)
- [Storybook](./.storybook/)
