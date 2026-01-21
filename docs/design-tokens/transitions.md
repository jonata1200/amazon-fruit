# ⚡ Design Tokens - Transições e Animações

## Visão Geral

O sistema de transições e animações garante movimentos suaves e consistentes em toda a interface, melhorando a experiência do usuário.

## Durações de Transição

| Token | Valor | Uso |
|-------|-------|-----|
| `instant` | `0ms` | Sem transição (mudanças instantâneas) |
| `fast` | `150ms` | Transições rápidas (hover, focus) |
| `base` | `200ms` | Transições padrão (mais comum) |
| `slow` | `300ms` | Transições lentas (modais, dropdowns) |
| `slower` | `500ms` | Transições muito lentas (animações complexas) |
| `slowest` | `700ms` | Transições extremamente lentas |

## Easing Functions

| Token | Valor | Uso |
|-------|-------|-----|
| `linear` | `linear` | Movimento constante |
| `in` | `cubic-bezier(0.4, 0, 1, 1)` | Acelera no final |
| `out` | `cubic-bezier(0, 0, 0.2, 1)` | Desacelera no final (recomendado) |
| `inOut` | `cubic-bezier(0.4, 0, 0.2, 1)` | Acelera e desacelera (mais comum) |
| `spring` | `cubic-bezier(0.68, -0.55, 0.265, 1.55)` | Movimento elástico |

## Delays

| Token | Valor | Uso |
|-------|-------|-----|
| `none` | `0ms` | Sem delay |
| `fast` | `50ms` | Delay rápido |
| `base` | `100ms` | Delay padrão |
| `slow` | `200ms` | Delay lento |
| `slower` | `300ms` | Delay muito lento |

## Transições por Componente

```typescript
import { componentTransitions } from '@/lib/design-tokens';

componentTransitions.color       // base + inOut - Cores
componentTransitions.background  // base + inOut - Backgrounds
componentTransitions.transform   // base + out - Transformações
componentTransitions.opacity     // fast + inOut - Opacidade
componentTransitions.shadow      // base + inOut - Sombras
componentTransitions.border      // fast + inOut - Bordas
```

## Animações Comuns

```typescript
import { animations } from '@/lib/design-tokens';

animations.fadeIn     // Fade in simples
animations.slideUp    // Desliza de baixo para cima
animations.slideDown  // Desliza de cima para baixo
animations.scaleIn    // Escala de pequeno para grande
```

## Uso em Tailwind CSS

### Durações

```tsx
<div className="transition-all duration-instant">  // 0ms
<div className="transition-all duration-fast">     // 150ms
<div className="transition-all duration-base">     // 200ms
<div className="transition-all duration-slow">    // 300ms
<div className="transition-all duration-slower">   // 500ms
<div className="transition-all duration-slowest">  // 700ms
```

### Easing

```tsx
<div className="ease-linear">    // linear
<div className="ease-in">        // in
<div className="ease-out">       // out
<div className="ease-in-out">    // inOut
```

### Transições Específicas

```tsx
<div className="transition-colors duration-base">
  {/* Transição apenas de cores */}
</div>

<div className="transition-transform duration-base">
  {/* Transição apenas de transform */}
</div>

<div className="transition-opacity duration-fast">
  {/* Transição apenas de opacidade */}
</div>
```

## Uso em JavaScript/TypeScript

```typescript
import { 
  getTransition, 
  componentTransitions,
  animations 
} from '@/lib/design-tokens';

// Obter duração específica
const duration = getTransition('duration', 'base'); // '200ms'

// Usar transição de componente
const colorTransition = componentTransitions.color;

// Aplicar programaticamente
element.style.transition = componentTransitions.color;
```

## Padrões de Uso

### Hover States

```tsx
<Button className="transition-colors duration-base hover:bg-primary/90">
  {/* Transição suave de cor em hover */}
</Button>
```

### Focus States

```tsx
<Input className="transition-all duration-fast focus:ring-2">
  {/* Transição rápida em foco */}
</Input>
```

### Modais e Dropdowns

```tsx
<Dialog className="transition-all duration-slow">
  {/* Transição mais lenta para modais */}
</Dialog>
```

### Loading States

```tsx
<Spinner className="animate-spin">
  {/* Animação contínua */}
</Spinner>
```

## Respeitando prefers-reduced-motion

```tsx
import { prefersReducedMotion, getRespectfulTransitionDuration } from '@/lib/utils/animations';

// Verificar preferência do usuário
const shouldReduceMotion = prefersReducedMotion();

// Obter duração respeitosa
const duration = getRespectfulTransitionDuration('base');
// Retorna '0ms' se prefers-reduced-motion estiver ativo
```

## Boas Práticas

1. **Use durações apropriadas**: Rápido para interações, lento para modais
2. **Prefira ease-out**: Cria sensação mais natural
3. **Respeite prefers-reduced-motion**: Sempre considere acessibilidade
4. **Mantenha consistência**: Use as mesmas durações para ações similares
5. **Evite animações excessivas**: Menos é mais

## Exemplos

```tsx
// ✅ Bom: Transição suave
<Button className="transition-colors duration-base hover:bg-primary/90">
  Ação
</Button>

// ❌ Ruim: Sem transição
<Button className="hover:bg-primary/90">
  Ação
</Button>

// ✅ Bom: Respeitando acessibilidade
import { prefersReducedMotion } from '@/lib/utils/animations';
const transition = prefersReducedMotion() 
  ? 'transition-none' 
  : 'transition-colors duration-base';

// ✅ Bom: Usando componente específico
import { componentTransitions } from '@/lib/design-tokens';
<div style={{ transition: componentTransitions.color }}>
  ...
</div>
```

---

**Referência**: `src/lib/design-tokens/transitions.ts`
