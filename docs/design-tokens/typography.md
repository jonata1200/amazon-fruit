# 📝 Design Tokens - Tipografia

## Visão Geral

O sistema tipográfico define fontes, tamanhos, pesos e espaçamentos para garantir hierarquia visual clara e legibilidade.

## Font Families

### Sans (Padrão)
```css
font-family: var(--font-geist-sans), system-ui, -apple-system, sans-serif;
```

### Mono
```css
font-family: var(--font-geist-mono), Menlo, Monaco, monospace;
```

### Serif
```css
font-family: Georgia, 'Times New Roman', serif;
```

## Tamanhos de Fonte

| Token | Valor | Pixels | Uso |
|-------|-------|--------|-----|
| `xs` | `0.75rem` | 12px | Captions, labels pequenos |
| `sm` | `0.875rem` | 14px | Texto secundário |
| `base` | `1rem` | 16px | **Texto padrão (body)** |
| `lg` | `1.125rem` | 18px | Texto destacado |
| `xl` | `1.25rem` | 20px | Subtítulos |
| `2xl` | `1.5rem` | 24px | H4 |
| `3xl` | `1.875rem` | 30px | H3 |
| `4xl` | `2.25rem` | 36px | H2 |
| `5xl` | `3rem` | 48px | H1 |
| `6xl` | `3.75rem` | 60px | Display |

## Pesos de Fonte

| Token | Valor | Uso |
|-------|-------|-----|
| `light` | 300 | Texto leve |
| `normal` | 400 | **Texto padrão** |
| `medium` | 500 | Texto médio |
| `semibold` | 600 | Subtítulos |
| `bold` | 700 | **Títulos** |
| `extrabold` | 800 | Títulos destacados |

## Line Heights

| Token | Valor | Uso |
|-------|-------|-----|
| `none` | 1 | Títulos compactos |
| `tight` | 1.25 | Títulos |
| `snug` | 1.375 | Subtítulos |
| `normal` | 1.5 | **Texto padrão** |
| `relaxed` | 1.625 | Texto longo |
| `loose` | 2 | Texto espaçado |

## Hierarquia Tipográfica

### Display / H1
```tsx
<Heading level="h1" className="text-5xl md:text-6xl font-bold leading-tight">
  Título Principal
</Heading>
```

### H2
```tsx
<Heading level="h2" className="text-4xl font-bold leading-snug">
  Subtítulo
</Heading>
```

### H3
```tsx
<Heading level="h3" className="text-3xl font-semibold leading-snug">
  Seção
</Heading>
```

### Body
```tsx
<Paragraph className="text-base leading-relaxed">
  Texto do corpo
</Paragraph>
```

### Small / Caption
```tsx
<Caption className="text-xs leading-normal">
  Texto auxiliar
</Caption>
```

## Uso em Tailwind

```tsx
// Tamanho e peso
<p className="text-lg font-semibold">

// Line height
<p className="leading-relaxed">

// Letter spacing
<p className="tracking-wide">

// Combinação
<h1 className="text-5xl font-bold leading-tight tracking-tight">
```

## Uso em JavaScript/TypeScript

```typescript
import { getTypography, getTypeScaleClasses } from '@/lib/utils';

// Obter valor
const fontSize = getTypography('fontSize', 'lg'); // '1.125rem'

// Obter classes
const classes = getTypeScaleClasses('h1');
// 'text-5xl font-bold leading-tight'
```

## Componentes Tipográficos

Use os componentes tipográficos para consistência:

```tsx
import { Heading, Paragraph, Text, Caption } from '@/components/typography';

<Heading level="h1">Título</Heading>
<Paragraph>Texto do parágrafo</Paragraph>
<Text size="lg" weight="semibold">Texto destacado</Text>
<Caption>Legenda</Caption>
```

## Acessibilidade

- **Tamanho mínimo**: 16px (1rem) para texto do corpo
- **Line height mínimo**: 1.5 para legibilidade
- **Contraste**: Garantir contraste WCAG AA
- **Hierarquia semântica**: Usar tags HTML corretas (h1-h6)

## Responsividade

Ajuste tamanhos de fonte para diferentes telas:

```tsx
<h1 className="text-3xl md:text-4xl lg:text-5xl">
  Título responsivo
</h1>
```

## Boas Práticas

1. **Use componentes tipográficos** ao invés de classes diretas
2. **Mantenha hierarquia clara** (h1 > h2 > h3 > body)
3. **Respeite tamanhos mínimos** para acessibilidade
4. **Use line-height adequado** para legibilidade
5. **Teste contraste** em diferentes backgrounds

## Exemplos

```tsx
// ✅ Bom: Usando componente
<Heading level="h1">Título</Heading>

// ❌ Ruim: Classes diretas sem semântica
<div className="text-5xl font-bold">Título</div>

// ✅ Bom: Hierarquia clara
<Heading level="h1">Principal</Heading>
<Heading level="h2">Subtítulo</Heading>
<Paragraph>Texto</Paragraph>

// ✅ Bom: Responsivo
<Heading level="h1" className="text-3xl md:text-5xl">
```
