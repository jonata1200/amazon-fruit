# 📚 Design Tokens - Sistema de Z-Index

## Visão Geral

O sistema de z-index usa camadas bem definidas para evitar conflitos e garantir que elementos sobrepostos apareçam na ordem correta.

## Camadas de Z-Index

| Camada | Valor | Uso |
|--------|-------|-----|
| `hide` | `-1` | Elementos ocultos (visually hidden) |
| `auto` | `auto` | Comportamento automático do navegador |
| `base` | `0` | Camada base, conteúdo normal |
| `docked` | `10` | Elementos fixos na tela (sidebar, navbar lateral) |
| `dropdown` | `1000` | Menus dropdown e seletores |
| `sticky` | `1100` | Elementos sticky (headers fixos) |
| `banner` | `1200` | Banners e notificações fixas |
| `overlay` | `1300` | Overlays e backdrops |
| `modal` | `1400` | Modais e diálogos |
| `popover` | `1500` | Popovers e tooltips flutuantes |
| `skipLink` | `1600` | Links de navegação rápida (acessibilidade) |
| `tooltip` | `1700` | Tooltips (mais alto que popovers) |

## Z-Index por Componente

### Componentes Específicos

```typescript
import { componentZIndex } from '@/lib/design-tokens';

// Componentes com z-index pré-definido
componentZIndex.sidebar    // 10 (docked)
componentZIndex.header      // 1100 (sticky)
componentZIndex.dropdown   // 1000
componentZIndex.tooltip    // 1700
componentZIndex.modal      // 1400
componentZIndex.popover    // 1500
componentZIndex.overlay    // 1300
componentZIndex.banner     // 1200
componentZIndex.skipLink   // 1600
```

## Uso em CSS/Tailwind

### Tailwind Classes

```tsx
// Usando classes Tailwind
<div className="z-50">        // z-index: 50 (custom)
<div className="z-dropdown">  // z-index: 1000
<div className="z-modal">     // z-index: 1400
```

### CSS Custom Properties

```css
/* Usando variáveis CSS */
.modal {
  z-index: var(--z-index-modal); /* 1400 */
}

.tooltip {
  z-index: var(--z-index-tooltip); /* 1700 */
}
```

## Uso em JavaScript/TypeScript

```typescript
import { zIndex, componentZIndex } from '@/lib/design-tokens';

// Acessar valores diretamente
const modalZ = zIndex.modal; // 1400
const tooltipZ = zIndex.tooltip; // 1700

// Usar z-index de componentes
const sidebarZ = componentZIndex.sidebar; // 10
const dropdownZ = componentZIndex.dropdown; // 1000

// Aplicar programaticamente
element.style.zIndex = String(zIndex.modal);
```

## Padrões de Uso

### Modal com Overlay

```tsx
// Overlay (backdrop)
<div className="fixed inset-0 z-overlay bg-background/80" />

// Modal
<div className="fixed inset-0 z-modal flex items-center justify-center">
  <div className="relative z-10">...</div>
</div>
```

### Dropdown Menu

```tsx
<div className="relative">
  <button>Trigger</button>
  <div className="absolute z-dropdown mt-2">...</div>
</div>
```

### Tooltip

```tsx
<div className="relative">
  <button>Hover me</button>
  <div className="absolute z-tooltip">Tooltip content</div>
</div>
```

### Sticky Header

```tsx
<header className="sticky top-0 z-sticky bg-background">
  Header content
</header>
```

### Sidebar

```tsx
<aside className="fixed left-0 top-0 h-full z-docked">
  Sidebar content
</aside>
```

## Hierarquia de Camadas

```
Tooltip (1700) ────────────────┐
  ↑                           │
Skip Link (1600) ─────────────┤ Mais alto
  ↑                           │
Popover (1500) ───────────────┤
  ↑                           │
Modal (1400) ─────────────────┤
  ↑                           │
Overlay (1300) ───────────────┤
  ↑                           │
Banner (1200) ────────────────┤
  ↑                           │
Sticky (1100) ────────────────┤
  ↑                           │
Dropdown (1000) ──────────────┤
  ↑                           │
Docked (10) ──────────────────┤
  ↑                           │
Base (0) ─────────────────────┘ Mais baixo
```

## Boas Práticas

1. **Use as camadas definidas**: Não crie valores customizados sem necessidade
2. **Respeite a hierarquia**: Modais sempre acima de overlays, tooltips acima de tudo
3. **Evite conflitos**: Use `componentZIndex` para componentes específicos
4. **Documente exceções**: Se precisar de um z-index customizado, documente o motivo
5. **Teste sobreposições**: Verifique que elementos aparecem na ordem correta

## Quando Criar Nova Camada

Crie uma nova camada apenas se:
- Não houver camada adequada existente
- A nova camada for usada em múltiplos lugares
- A hierarquia atual não suportar o caso de uso

## Exemplos de Uso

```tsx
// ✅ Bom: Usando camada definida
<div className="z-modal">...</div>

// ❌ Ruim: Valor arbitrário
<div className="z-[9999]">...</div>

// ✅ Bom: Usando componente específico
import { componentZIndex } from '@/lib/design-tokens';
<div style={{ zIndex: componentZIndex.modal }}>...</div>

// ✅ Bom: Múltiplas camadas
<div className="relative z-base">
  <div className="absolute z-dropdown">...</div>
  <div className="absolute z-tooltip">...</div>
</div>
```

## Troubleshooting

### Elemento não aparece acima de outro

1. Verifique se está usando a camada correta
2. Confirme que o elemento pai não tem `z-index` que limita o filho
3. Verifique se há `position: relative/absolute/fixed` no elemento

### Conflitos de z-index

1. Use `componentZIndex` para componentes específicos
2. Documente qualquer z-index customizado
3. Considere refatorar se houver muitos valores customizados

---

**Referência**: `src/lib/design-tokens/z-index.ts`
