# ⚡ Guia de Uso do Tailwind CSS

## Visão Geral

Este projeto usa Tailwind CSS v4 com configuração otimizada e plugins customizados.

## Configuração

O Tailwind está configurado em `tailwind.config.ts` com:
- Design tokens integrados
- Plugins customizados
- Variantes customizadas
- Dark mode suportado

## Utilitários Customizados

### Espaçamento
```tsx
<div className="spacing-xs">  // gap-1
<div className="spacing-md">  // gap-4
<div className="spacing-lg">  // gap-6
```

### Elevação
```tsx
<div className="elevation-1">  // shadow-sm
<div className="elevation-3">  // shadow-md
<div className="elevation-5">  // shadow-xl
```

### Container Responsivo
```tsx
<div className="container-responsive">
  Container com max-width responsivo
</div>
```

### Text Balance
```tsx
<p className="text-balance">
  Texto com balanceamento automático
</p>
```

### Scrollbar Thin
```tsx
<div className="scrollbar-thin overflow-auto">
  Scrollbar estilizada
</div>
```

### Focus Ring
```tsx
<button className="focus-ring">
  Botão com focus visível
</button>
```

### Truncate Multi-line
```tsx
<p className="truncate-2">  // 2 linhas
<p className="truncate-3">  // 3 linhas
```

## Animações Customizadas

```tsx
<div className="animate-fade-in">
<div className="animate-slide-up">
<div className="animate-scale-in">
```

## Variantes Customizadas

### Hover Touch
```tsx
<div className="hover-touch:hover:bg-accent">
  Apenas em dispositivos com hover
</div>
```

### Reduced Motion
```tsx
<div className="reduced-motion:animate-none">
  Respeita prefers-reduced-motion
</div>
```

### Print
```tsx
<div className="print:hidden">
  Esconde na impressão
</div>
```

## Plugins Customizados

### Design Tokens Plugin
Adiciona utilitários baseados em design tokens.

### Utilities Plugin
Adiciona utilitários comuns (container-responsive, text-balance, etc).

### Animations Plugin
Adiciona animações customizadas (fade-in, slide-up, scale-in).

## Função `cn()`

Use `cn()` para combinar classes:

```tsx
import { cn } from '@/lib/utils';

<div className={cn(
  'base-class',
  condition && 'conditional-class',
  variant === 'primary' && 'primary-class'
)}>
```

## Boas Práticas

1. **Use design tokens** ao invés de valores arbitrários
2. **Combine classes com `cn()`** para melhor legibilidade
3. **Use variantes customizadas** quando apropriado
4. **Respeite dark mode** usando variáveis CSS
5. **Otimize para produção** (Tailwind faz tree-shaking automático)

## Convenções

- **Cores**: Use cores semânticas (`bg-primary`, `text-foreground`)
- **Espaçamento**: Use escala base (`p-4`, `gap-6`)
- **Tipografia**: Use componentes tipográficos quando possível
- **Responsividade**: Mobile-first (`md:`, `lg:`)

## Exemplos

```tsx
// ✅ Bom: Usando tokens
<div className="bg-primary-600 p-4 gap-4">

// ❌ Ruim: Valores arbitrários
<div className="bg-[#9333ea] p-[13px] gap-[17px]">

// ✅ Bom: Com cn()
<div className={cn('base', isActive && 'active')}>

// ✅ Bom: Responsivo
<div className="p-4 md:p-6 lg:p-8">
```
