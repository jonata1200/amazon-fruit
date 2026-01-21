# 🛠️ Guia de Utilitários

## Visão Geral

Este guia documenta todos os utilitários e helpers disponíveis no design system para facilitar o desenvolvimento.

## Funções de Transformação

### Transformar Tokens em Classes Tailwind

```typescript
import { 
  spacingToTailwindClass,
  shadowToTailwindClass,
  radiusToTailwindClass,
  tokensToTailwindClasses 
} from '@/lib/utils/transformations';

// Espaçamento
const paddingClass = spacingToTailwindClass('md', 'p'); // 'p-4'
const marginClass = spacingToTailwindClass('lg', 'm'); // 'm-6'

// Sombras
const shadowClass = shadowToTailwindClass('md'); // 'shadow-md'

// Border Radius
const radiusClass = radiusToTailwindClass('lg'); // 'rounded-lg'

// Múltiplos tokens
const classes = tokensToTailwindClasses({
  padding: 'md',
  gap: 'sm',
  shadow: 'base',
  radius: 'md'
});
// 'p-4 gap-2 shadow rounded-md'
```

### Gerar CSS Custom Properties

```typescript
import { tokensToCSSVariables } from '@/lib/utils/transformations';

const css = tokensToCSSVariables();
// Gera :root { --color-primary-600: #9333ea; ... }
```

## Utilitários de Performance

### Debounce e Throttle

```typescript
import { debounce, throttle, useDebounceValue, useThrottleValue } from '@/lib/utils/performance';

// Debounce function
const debouncedSearch = debounce((query: string) => {
  // Buscar...
}, 300);

// Throttle function
const throttledScroll = throttle(() => {
  // Atualizar posição...
}, 100);

// Hooks
const debouncedInput = useDebounceValue(inputValue, 300);
const throttledScroll = useThrottleValue(scrollPosition, 100);
```

### Memoização

```typescript
import { 
  useMemoizedValue, 
  useMemoizedCallback,
  optimizeComponent 
} from '@/lib/utils/performance';

// Memoizar valor calculado
const expensiveValue = useMemoizedValue(() => {
  return heavyCalculation(data);
}, [data]);

// Memoizar callback
const handleClick = useMemoizedCallback(() => {
  // Ação
}, [deps]);

// Otimizar componente
const OptimizedCard = optimizeComponent(Card);
```

### Lazy Loading

```typescript
import { createLazyComponent, useLazyImage } from '@/lib/utils/performance';

// Componente lazy
const HeavyChart = createLazyComponent(() => import('./HeavyChart'));

// Imagem lazy
const { src, isLoading, error } = useLazyImage('/image.jpg', '/placeholder.jpg');
```

## Utilitários de Desenvolvimento

### Logging

```typescript
import { devLogger } from '@/lib/utils/development';

// Logs (apenas em desenvolvimento)
devLogger.log('Mensagem de log');
devLogger.warn('Aviso');
devLogger.error('Erro');

// Agrupar logs
devLogger.group('Grupo de logs', () => {
  devLogger.log('Item 1');
  devLogger.log('Item 2');
});

// Tabela
devLogger.table(data);
```

### Validação de Props

```typescript
import { validateProps } from '@/lib/utils/development';

function MyComponent({ value, count }: Props) {
  validateProps('MyComponent', { value, count }, {
    value: (v) => typeof v === 'string',
    count: (c) => typeof c === 'number' && c >= 0,
  });
  
  // ...
}
```

### Debug

```typescript
import { debugValue, measurePerformance, debugRenders } from '@/lib/utils/development';

// Inspecionar valor
const result = debugValue('My Value', complexObject);

// Medir performance
const result = measurePerformance('Heavy Calculation', () => {
  return expensiveOperation();
});

// Debug de renders
debugRenders('MyComponent', { prop1, prop2 });
```

### Warnings

```typescript
import { warnDeprecatedProps } from '@/lib/utils/development';

function MyComponent({ oldProp, newProp }: Props) {
  warnDeprecatedProps('MyComponent', ['oldProp'], {
    oldProp: 'newProp'
  });
  
  // ...
}
```

## Helpers de Design Tokens

### Acessar Tokens

```typescript
import { 
  getColor, 
  getSpacing, 
  getTypography,
  getShadow,
  getRadius 
} from '@/lib/utils';

// Cores
const primary = getColor('primary', 600);

// Espaçamento
const padding = getSpacing('md');

// Tipografia
const fontSize = getTypography('fontSize', 'base');

// Sombras
const shadow = getShadow('md');

// Border Radius
const radius = getRadius('lg');
```

### Hooks para Tokens

```typescript
import { 
  useDesignToken,
  useColor,
  useSpacing,
  useTypography 
} from '@/lib/hooks/use-design-token';

// Token genérico
const color = useDesignToken('colors.primary.600');

// Tokens específicos
const primary = useColor('primary', 600);
const padding = useSpacing('md');
const fontSize = useTypography('fontSize', 'base');
```

## Utilitários de Cores

```typescript
import { 
  getColorWithOpacity,
  getContrastRatio,
  meetsContrastRatio,
  getTextColor,
  generateColorPalette 
} from '@/lib/utils/colors';

// Cor com opacidade
const transparent = getColorWithOpacity('primary', 600, 0.5);

// Contraste
const ratio = getContrastRatio('#000', '#fff');
const isAccessible = meetsContrastRatio('#000', '#fff', 'AA');

// Cor de texto adequada
const textColor = getTextColor('#9333ea'); // '#ffffff' ou '#000000'

// Gerar paleta
const palette = generateColorPalette('#9333ea');
```

## Utilitários de Espaçamento

```typescript
import { 
  getSpacing,
  calculateSpacing,
  getPaddingClasses,
  getMarginClasses 
} from '@/lib/utils/spacing';

// Obter valor
const spacing = getSpacing('md');

// Calcular
const calculated = calculateSpacing(2, 'md'); // 2 * md

// Classes Tailwind
const padding = getPaddingClasses('md'); // 'p-4'
const margin = getMarginClasses('lg'); // 'm-6'
```

## Utilitários de Acessibilidade

```typescript
import { 
  generateId,
  createAriaAttributes,
  createFocusAttributes,
  srOnly 
} from '@/lib/utils/accessibility';

// ID único
const id = generateId('input');

// ARIA attributes
const aria = createAriaAttributes({
  label: 'Email',
  describedBy: 'email-hint',
  invalid: true
});

// Focus attributes
const focus = createFocusAttributes(true);

// Screen reader only
<div className={srOnly}>Texto apenas para leitores de tela</div>
```

## Utilitários de Animações

```typescript
import { 
  prefersReducedMotion,
  getRespectfulTransitionDuration,
  getTransitionClasses 
} from '@/lib/utils/animations';

// Verificar preferência
const shouldReduce = prefersReducedMotion();

// Duração respeitosa
const duration = getRespectfulTransitionDuration('base');

// Classes de transição
const transition = getTransitionClasses(['color', 'background'], 'base', 'inOut');
```

## Boas Práticas

1. **Use utilitários apropriados**: Escolha o utilitário certo para cada situação
2. **Performance**: Use memoização e lazy loading para componentes pesados
3. **Desenvolvimento**: Use devLogger apenas em desenvolvimento
4. **Acessibilidade**: Sempre valide contraste e use helpers de acessibilidade
5. **Type-safety**: Aproveite os tipos TypeScript dos utilitários

---

**Referência**: 
- `src/lib/utils/` - Todos os utilitários
- `src/lib/hooks/` - Hooks customizados
