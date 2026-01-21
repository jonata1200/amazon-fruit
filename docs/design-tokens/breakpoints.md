# 📱 Design Tokens - Breakpoints e Responsividade

## Visão Geral

O sistema de breakpoints está alinhado com o Tailwind CSS padrão, garantindo consistência entre utilitários CSS e media queries JavaScript.

## Breakpoints Disponíveis

| Breakpoint | Valor | Pixels | Uso |
|------------|-------|--------|-----|
| `sm` | `640px` | 640px | Tablets pequenos, telas grandes de celular |
| `md` | `768px` | 768px | Tablets, telas médias |
| `lg` | `1024px` | 1024px | Laptops, desktops pequenos |
| `xl` | `1280px` | 1280px | Desktops médios |
| `2xl` | `1536px` | 1536px | Desktops grandes, telas wide |

## Container Widths

Larguras máximas recomendadas para containers em cada breakpoint:

| Breakpoint | Container Width | Uso |
|------------|-----------------|-----|
| `sm` | `640px` | Conteúdo em tablets pequenos |
| `md` | `768px` | Conteúdo em tablets |
| `lg` | `1024px` | Conteúdo em laptops |
| `xl` | `1280px` | Conteúdo em desktops |
| `2xl` | `1536px` | Conteúdo em telas grandes |
| `full` | `100%` | Largura total |

## Uso em Tailwind CSS

### Classes Responsivas

```tsx
// Aplicar estilos em breakpoints específicos
<div className="text-sm md:text-base lg:text-lg">
  Texto que aumenta em telas maiores
</div>

// Grid responsivo
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  Grid que adapta número de colunas
</div>

// Espaçamento responsivo
<div className="p-4 md:p-6 lg:p-8">
  Padding que aumenta em telas maiores
</div>

// Visibilidade responsiva
<div className="hidden md:block">
  Visível apenas em telas médias e maiores
</div>
```

### Breakpoints Customizados

```tsx
// Usar breakpoints específicos
<div className="sm:text-sm md:text-base lg:text-lg xl:text-xl">
  Texto que escala em cada breakpoint
</div>
```

## Uso em JavaScript/TypeScript

### Media Queries

```typescript
import { mediaQueries, breakpoints } from '@/lib/design-tokens';

// Verificar se está em um breakpoint específico
const isMobile = window.matchMedia(mediaQueries.maxSm).matches;
const isTablet = window.matchMedia(mediaQueries.md).matches;
const isDesktop = window.matchMedia(mediaQueries.lg).matches;

// Usar em useEffect
React.useEffect(() => {
  const mediaQuery = window.matchMedia(mediaQueries.md);
  const handleChange = (e: MediaQueryListEvent) => {
    if (e.matches) {
      // Tela média ou maior
    }
  };
  
  mediaQuery.addEventListener('change', handleChange);
  return () => mediaQuery.removeEventListener('change', handleChange);
}, []);
```

### Hooks Customizados

```typescript
import { useBreakpoint, useCurrentBreakpoint } from '@/lib/hooks/use-breakpoint';

// Hook para verificar breakpoint
const isMobile = useBreakpoint('md', 'below'); // true se < 768px
const isDesktop = useBreakpoint('lg', 'above'); // true se >= 1024px

// Hook para breakpoint atual
const currentBreakpoint = useCurrentBreakpoint(); // 'sm' | 'md' | 'lg' | 'xl' | '2xl'
```

## Padrões de Layout Responsivo

### Mobile First

Sempre comece com estilos mobile e adicione breakpoints maiores:

```tsx
// ✅ Bom: Mobile first
<div className="p-4 md:p-6 lg:p-8">
  Padding que aumenta em telas maiores
</div>

// ❌ Ruim: Desktop first
<div className="p-8 lg:p-6 md:p-4">
  Padding que diminui (não recomendado)
</div>
```

### Grid Responsivo

```tsx
// Grid que adapta número de colunas
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {/* 1 coluna mobile, 2 tablets, 3 laptops, 4 desktops */}
</div>
```

### Tipografia Responsiva

```tsx
// Texto que escala com o breakpoint
<h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl">
  Título responsivo
</h1>
```

### Espaçamento Responsivo

```tsx
// Espaçamento que aumenta em telas maiores
<div className="p-4 md:p-6 lg:p-8 xl:p-12">
  Conteúdo com padding responsivo
</div>
```

## Container Responsivo

```tsx
// Container que limita largura máxima
<div className="container mx-auto px-4 sm:px-6 lg:px-8">
  {/* 
    - Largura máxima baseada no breakpoint
    - Padding horizontal que aumenta em telas maiores
  */}
</div>
```

## Padrões por Tipo de Componente

### Cards

```tsx
// Cards que mudam layout em telas maiores
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <Card />
  <Card />
  <Card />
</div>
```

### Navegação

```tsx
// Menu que muda de hamburger para horizontal
<nav className="flex flex-col md:flex-row gap-4">
  {/* Mobile: vertical, Desktop: horizontal */}
</nav>
```

### Formulários

```tsx
// Formulário que muda de 1 para 2 colunas
<form className="grid grid-cols-1 md:grid-cols-2 gap-4">
  <Input />
  <Input />
</form>
```

### Tabelas

```tsx
// Tabela que vira cards em mobile
<div className="block md:table">
  {/* Mobile: cards, Desktop: tabela */}
</div>
```

## Media Queries Disponíveis

### Min Width (Mobile First)

```typescript
mediaQueries.sm    // (min-width: 640px)
mediaQueries.md    // (min-width: 768px)
mediaQueries.lg    // (min-width: 1024px)
mediaQueries.xl    // (min-width: 1280px)
mediaQueries['2xl'] // (min-width: 1536px)
```

### Max Width (Desktop First)

```typescript
mediaQueries.maxSm // (max-width: 639px)
mediaQueries.maxMd // (max-width: 767px)
mediaQueries.maxLg // (max-width: 1023px)
mediaQueries.maxXl // (max-width: 1279px)
```

## Boas Práticas

1. **Mobile First**: Sempre comece com estilos mobile
2. **Use breakpoints definidos**: Não crie breakpoints customizados sem necessidade
3. **Teste em diferentes tamanhos**: Verifique em cada breakpoint
4. **Considere touch targets**: Em mobile, elementos devem ter pelo menos 44x44px
5. **Otimize imagens**: Use imagens responsivas com `srcset`
6. **Evite muitos breakpoints**: Use apenas os necessários

## Exemplos de Uso

```tsx
// ✅ Bom: Mobile first
<div className="p-4 md:p-6 lg:p-8">

// ❌ Ruim: Desktop first
<div className="p-8 lg:p-6 md:p-4">

// ✅ Bom: Grid responsivo
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">

// ✅ Bom: Visibilidade responsiva
<div className="hidden md:block">
  Visível apenas em telas médias+
</div>

// ✅ Bom: Usando hooks
const isMobile = useBreakpoint('md', 'below');
{isMobile ? <MobileMenu /> : <DesktopMenu />}
```

## Troubleshooting

### Estilos não aplicam em breakpoint

1. Verifique se está usando a sintaxe correta: `md:classe`
2. Confirme que o breakpoint está correto
3. Verifique se há conflitos de especificidade CSS

### Layout quebra em breakpoints intermediários

1. Teste em tamanhos intermediários (ex: 900px entre md e lg)
2. Considere adicionar breakpoint intermediário se necessário
3. Use valores fluidos quando possível (`clamp()`)

---

**Referência**: `src/lib/design-tokens/breakpoints.ts`
