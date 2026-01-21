# 🌑 Design Tokens - Sistema de Sombras e Elevação

## Visão Geral

O sistema de sombras cria hierarquia visual e profundidade, ajudando a organizar elementos na interface. As sombras são ajustadas para modo claro e escuro.

## Níveis de Elevação

| Nível | Sombra | Uso |
|-------|--------|-----|
| `0` | `none` | Sem elevação, elementos no mesmo plano |
| `1` | `sm` | Elementos levemente elevados (botões, badges) |
| `2` | `base` | Elementos padrão (cards, inputs) |
| `3` | `md` | Elementos destacados (cards hover, dropdowns) |
| `4` | `lg` | Elementos muito elevados (modals, popovers) |
| `5` | `xl` | Elementos extremamente elevados (tooltips) |

## Sombras Disponíveis

### Modo Claro

| Token | Valor | Uso |
|-------|-------|-----|
| `none` | `none` | Sem sombra |
| `sm` | `0 1px 2px 0 rgb(0 0 0 / 0.05)` | Sombras sutis |
| `base` | `0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)` | Sombras padrão |
| `md` | `0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)` | Sombras médias |
| `lg` | `0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)` | Sombras grandes |
| `xl` | `0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)` | Sombras extra grandes |
| `2xl` | `0 25px 50px -12px rgb(0 0 0 / 0.25)` | Sombras enormes |
| `inner` | `inset 0 2px 4px 0 rgb(0 0 0 / 0.05)` | Sombras internas (inputs) |

### Modo Escuro

No modo escuro, as sombras são mais intensas para manter visibilidade:

- Opacidade aumentada (0.3-0.5 ao invés de 0.05-0.25)
- Mantém a mesma estrutura para consistência

## Uso em Tailwind CSS

```tsx
// Classes Tailwind padrão
<div className="shadow-sm">   // sm
<div className="shadow-md">   // md
<div className="shadow-lg">   // lg
<div className="shadow-xl">   // xl
<div className="shadow-2xl">  // 2xl
<div className="shadow-none"> // none
<div className="shadow-inner"> // inner
```

## Uso em JavaScript/TypeScript

```typescript
import { getShadow, elevation, componentShadows } from '@/lib/design-tokens';

// Obter sombra específica
const shadow = getShadow('md'); // '0 4px 6px -1px...'

// Usar nível de elevação
const cardShadow = elevation[2]; // base

// Usar sombra de componente
const modalShadow = componentShadows.modal; // 2xl
```

## Sombras por Componente

### Componentes Específicos

```typescript
import { componentShadows } from '@/lib/design-tokens';

componentShadows.card         // base - Cards padrão
componentShadows.cardHover    // md - Cards em hover
componentShadows.modal        // 2xl - Modais
componentShadows.dropdown     // lg - Dropdowns
componentShadows.tooltip      // md - Tooltips
componentShadows.button       // sm - Botões
componentShadows.buttonHover  // base - Botões em hover
componentShadows.input        // inner - Inputs
componentShadows.inputFocus  // base - Inputs em foco
```

## Padrões de Uso

### Cards

```tsx
// Card padrão
<Card className="shadow-base">...</Card>

// Card em hover
<Card className="shadow-base hover:shadow-md transition-shadow">
  ...
</Card>
```

### Modais

```tsx
<Dialog className="shadow-2xl">
  {/* Modal com sombra máxima */}
</Dialog>
```

### Botões

```tsx
<Button className="shadow-sm hover:shadow-base">
  {/* Sombra sutil que aumenta em hover */}
</Button>
```

### Inputs

```tsx
<Input className="shadow-inner focus:shadow-base">
  {/* Sombra interna que muda em foco */}
</Input>
```

## Boas Práticas

1. **Use elevação consistentemente**: Elementos similares devem ter a mesma elevação
2. **Respeite a hierarquia**: Elementos mais importantes devem ter mais elevação
3. **Considere dark mode**: Sombras são ajustadas automaticamente
4. **Evite sombras excessivas**: Use apenas quando necessário para hierarquia
5. **Teste contraste**: Garanta que elementos com sombra ainda têm contraste adequado

## Exemplos

```tsx
// ✅ Bom: Elevação consistente
<Card className="shadow-base">
  <Button className="shadow-sm">Ação</Button>
</Card>

// ❌ Ruim: Elevação inconsistente
<Card className="shadow-2xl">
  <Button className="shadow-2xl">Ação</Button>
</Card>

// ✅ Bom: Transição suave
<div className="shadow-base hover:shadow-md transition-shadow">
  ...
</div>

// ✅ Bom: Usando componente específico
import { componentShadows } from '@/lib/design-tokens';
<div style={{ boxShadow: componentShadows.modal }}>
  ...
</div>
```

---

**Referência**: `src/lib/design-tokens/shadows.ts`
