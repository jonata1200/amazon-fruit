# 📏 Design Tokens - Espaçamento

## Visão Geral

O sistema de espaçamento usa uma escala baseada em 4px (0.25rem), garantindo consistência visual em todo o design system.

## Escala Base

| Token | Valor | Pixels | Uso |
|-------|-------|--------|-----|
| `xs` | `0.25rem` | 4px | Espaçamento mínimo |
| `sm` | `0.5rem` | 8px | Espaçamento pequeno |
| `md` | `1rem` | 16px | Espaçamento padrão |
| `lg` | `1.5rem` | 24px | Espaçamento grande |
| `xl` | `2rem` | 32px | Espaçamento extra grande |
| `2xl` | `3rem` | 48px | Espaçamento muito grande |
| `3xl` | `4rem` | 64px | Espaçamento enorme |
| `4xl` | `6rem` | 96px | Espaçamento máximo |
| `5xl` | `8rem` | 128px | Espaçamento extremo |

## Uso em Tailwind

```tsx
// Padding
<div className="p-4">        // md (16px)
<div className="p-6">        // lg (24px)
<div className="px-4 py-2">  // Padding assimétrico

// Margin
<div className="m-4">        // md (16px)
<div className="mt-8">       // xl (32px)

// Gap
<div className="flex gap-4"> // md (16px)
```

## Uso em JavaScript/TypeScript

```typescript
import { getSpacing, getPaddingClasses } from '@/lib/utils';

// Obter valor
const spacing = getSpacing('md'); // '1rem'

// Obter classes Tailwind
const paddingClass = getPaddingClasses('md'); // 'p-4'

// Espaçamento responsivo
const responsiveSpacing = getResponsiveSpacing('sm', 'lg');
// 'p-2 md:p-6'
```

## Espaçamento Semântico

Para componentes, use espaçamento semântico:

- **Tight**: `gap-2` (8px) - Elementos relacionados
- **Normal**: `gap-4` (16px) - Espaçamento padrão
- **Loose**: `gap-6` (24px) - Elementos separados
- **Extra Loose**: `gap-8` (32px) - Seções diferentes

## Padrões de Layout

### Cards
```tsx
<Card className="p-6">        // Padding interno
  <CardHeader className="pb-4"> // Espaçamento entre header e content
    <CardTitle />
  </CardHeader>
  <CardContent className="pt-0"> // Remove padding top
    ...
  </CardContent>
</Card>
```

### Formulários
```tsx
<div className="space-y-4">  // Espaçamento vertical entre campos
  <Input />
  <Input />
  <Button />
</div>
```

### Grids
```tsx
<div className="grid grid-cols-3 gap-4">  // Gap entre itens
  ...
</div>
```

## Responsividade

Use espaçamento responsivo para diferentes tamanhos de tela:

```tsx
<div className="p-4 md:p-6 lg:p-8">
  Padding que aumenta em telas maiores
</div>
```

## Boas Práticas

1. **Use a escala base** ao invés de valores arbitrários
2. **Mantenha consistência** entre elementos similares
3. **Use espaçamento semântico** para componentes
4. **Considere responsividade** em layouts
5. **Evite espaçamento negativo** quando possível

## Exemplos

```tsx
// ✅ Bom: Usando escala
<div className="p-4 gap-4">

// ❌ Ruim: Valor arbitrário
<div className="p-[13px] gap-[17px]">

// ✅ Bom: Semântico
<div className="space-y-4">

// ✅ Bom: Responsivo
<div className="p-4 md:p-6 lg:p-8">
```
