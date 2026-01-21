# 🔲 Design Tokens - Bordas e Border Radius

## Visão Geral

O sistema de bordas e border radius garante consistência visual em todos os componentes, criando uma identidade visual coesa.

## Border Radius

| Token | Valor | Pixels | Uso |
|-------|-------|--------|-----|
| `none` | `0` | 0px | Sem arredondamento |
| `sm` | `0.125rem` | 2px | Arredondamento mínimo |
| `base` | `0.25rem` | 4px | Arredondamento pequeno |
| `md` | `0.375rem` | 6px | Arredondamento padrão |
| `lg` | `0.5rem` | 8px | Arredondamento grande |
| `xl` | `0.75rem` | 12px | Arredondamento extra grande |
| `2xl` | `1rem` | 16px | Arredondamento muito grande |
| `3xl` | `1.5rem` | 24px | Arredondamento enorme |
| `full` | `9999px` | - | Totalmente arredondado (círculo) |

## Border Radius por Componente

```typescript
import { componentRadius } from '@/lib/design-tokens';

componentRadius.button   // md (6px) - Botões
componentRadius.input    // md (6px) - Inputs
componentRadius.card     // lg (8px) - Cards
componentRadius.modal    // xl (12px) - Modais
componentRadius.tooltip  // md (6px) - Tooltips
componentRadius.badge    // full - Badges circulares
componentRadius.avatar   // full - Avatares circulares
```

## Larguras de Borda

| Token | Valor | Uso |
|-------|-------|-----|
| `0` | `0` | Sem borda |
| `1` | `1px` | Borda fina |
| `2` | `2px` | Borda padrão |
| `4` | `4px` | Borda grossa |
| `8` | `8px` | Borda muito grossa |

## Estilos de Borda

| Token | Valor | Uso |
|-------|-------|-----|
| `solid` | `solid` | Borda sólida (padrão) |
| `dashed` | `dashed` | Borda tracejada |
| `dotted` | `dotted` | Borda pontilhada |
| `none` | `none` | Sem borda |

## Uso em Tailwind CSS

### Border Radius

```tsx
// Classes Tailwind padrão
<div className="rounded-none">  // none
<div className="rounded-sm">    // sm
<div className="rounded">      // base
<div className="rounded-md">   // md
<div className="rounded-lg">   // lg
<div className="rounded-xl">   // xl
<div className="rounded-2xl">   // 2xl
<div className="rounded-3xl">  // 3xl
<div className="rounded-full">  // full

// Border radius específico
<div className="rounded-t-lg">  // top
<div className="rounded-r-lg">  // right
<div className="rounded-b-lg">  // bottom
<div className="rounded-l-lg">  // left
```

### Border Width

```tsx
<div className="border-0">   // 0
<div className="border">     // 1px
<div className="border-2">   // 2px
<div className="border-4">   // 4px
<div className="border-8">   // 8px
```

### Border Style

```tsx
<div className="border-solid">  // solid
<div className="border-dashed"> // dashed
<div className="border-dotted"> // dotted
<div className="border-none">   // none
```

## Uso em JavaScript/TypeScript

```typescript
import { getRadius, borderRadius, componentRadius } from '@/lib/design-tokens';

// Obter radius específico
const radius = getRadius('lg'); // '0.5rem'

// Usar radius de componente
const buttonRadius = componentRadius.button; // '0.375rem'

// Aplicar programaticamente
element.style.borderRadius = borderRadius.lg;
```

## Padrões de Uso

### Botões

```tsx
<Button className="rounded-md">
  {/* Border radius padrão para botões */}
</Button>
```

### Inputs

```tsx
<Input className="rounded-md">
  {/* Border radius padrão para inputs */}
</Input>
```

### Cards

```tsx
<Card className="rounded-lg">
  {/* Border radius maior para cards */}
</Card>
```

### Modais

```tsx
<Dialog className="rounded-xl">
  {/* Border radius grande para modais */}
</Dialog>
```

### Badges e Avatares

```tsx
<Badge className="rounded-full">
  {/* Totalmente arredondado */}
</Badge>

<Avatar className="rounded-full">
  {/* Círculo perfeito */}
</Avatar>
```

## Boas Práticas

1. **Use radius consistentemente**: Componentes similares devem ter o mesmo radius
2. **Respeite a hierarquia**: Elementos maiores podem ter radius maiores
3. **Considere o contexto**: Cards podem ter radius maiores que botões
4. **Evite radius excessivos**: Use `full` apenas quando necessário (badges, avatares)
5. **Mantenha proporção**: Radius deve ser proporcional ao tamanho do elemento

## Exemplos

```tsx
// ✅ Bom: Radius consistente
<Button className="rounded-md">Ação</Button>
<Input className="rounded-md" />

// ❌ Ruim: Radius inconsistente
<Button className="rounded-full">Ação</Button>
<Input className="rounded-none" />

// ✅ Bom: Usando componente específico
import { componentRadius } from '@/lib/design-tokens';
<div style={{ borderRadius: componentRadius.card }}>
  ...
</div>

// ✅ Bom: Radius condicional
<div className={cn("rounded-md", isCompact && "rounded-sm")}>
  ...
</div>
```

---

**Referência**: `src/lib/design-tokens/borders.ts`
