# ⚡ Guia de Performance

## Visão Geral

Este guia documenta as otimizações de performance implementadas no design system e melhores práticas para manter a aplicação rápida.

## Otimizações do Tailwind CSS

### JIT Mode

O Tailwind v4 usa JIT (Just-In-Time) por padrão, gerando apenas as classes usadas:

```typescript
// tailwind.config.ts
// JIT está ativo automaticamente
// Apenas classes usadas são incluídas no bundle final
```

### Content Paths Otimizados

```typescript
content: [
  './src/**/*.{js,ts,jsx,tsx,mdx}',
  // Exclusões para melhor performance
  '!./src/**/*.test.{js,ts,jsx,tsx}',
  '!./node_modules/**',
  '!./.next/**',
]
```

### Purge/Tree-shaking

O Tailwind automaticamente remove classes não utilizadas no build de produção.

## Otimizações de Componentes

### Lazy Loading

```tsx
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<LoadingScreen />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Memoização

```tsx
import { memo, useMemo } from 'react';

// Memoizar componentes pesados
const ExpensiveComponent = memo(({ data }) => {
  // Componente que só re-renderiza se props mudarem
});

// Memoizar cálculos caros
const expensiveValue = useMemo(() => {
  return heavyCalculation(data);
}, [data]);
```

### Code Splitting

```tsx
// Dividir código em chunks menores
const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));
```

## Otimizações de CSS

### Minificação

O Next.js minifica CSS automaticamente em produção:

```bash
npm run build
# CSS é minificado automaticamente
```

### Critical CSS

O Next.js extrai CSS crítico automaticamente para melhor First Contentful Paint.

## Otimizações de Imagens

### Next.js Image

```tsx
import Image from 'next/image';

<Image
  src="/image.jpg"
  width={500}
  height={300}
  alt="Descrição"
  loading="lazy"
  // Otimizações automáticas
/>
```

## Bundle Size

### Analisar Bundle

```bash
# Analisar tamanho do bundle
npm run build
# Verificar output em .next/analyze
```

### Tree-shaking

```typescript
// ✅ Bom: Import específico
import { Button } from '@/components/ui';

// ❌ Ruim: Import de tudo
import * from '@/components/ui';
```

## Performance de Renderização

### Evitar Re-renders Desnecessários

```tsx
// Use React.memo para componentes pesados
const Card = memo(({ title, content }) => {
  return <div>...</div>;
});

// Use useMemo para valores calculados
const sortedData = useMemo(() => {
  return data.sort(/* ... */);
}, [data]);
```

### Debounce e Throttle

```tsx
import { useDebounce } from '@/lib/hooks/useDebounce';

const debouncedValue = useDebounce(value, 300);
```

## Métricas de Performance

### Web Vitals

O projeto já inclui utilitários para medir Web Vitals:

```typescript
import { reportWebVitals } from '@/lib/utils/web-vitals';

// Reporta métricas automaticamente
reportWebVitals(console.log);
```

### Core Web Vitals

- **LCP (Largest Contentful Paint)**: < 2.5s
- **FID (First Input Delay)**: < 100ms
- **CLS (Cumulative Layout Shift)**: < 0.1

## Boas Práticas

### 1. Use Design Tokens

```tsx
// ✅ Bom: Usa tokens (otimizado)
<div className="p-4 gap-4">

// ❌ Ruim: Valores arbitrários
<div className="p-[17px] gap-[23px]">
```

### 2. Evite Inline Styles

```tsx
// ✅ Bom: Classes Tailwind
<div className="bg-primary text-white">

// ❌ Ruim: Inline styles
<div style={{ backgroundColor: '#9333ea', color: '#fff' }}>
```

### 3. Lazy Load Componentes Pesados

```tsx
// ✅ Bom: Lazy loading
const Chart = lazy(() => import('./Chart'));

// ❌ Ruim: Import direto de componente pesado
import Chart from './Chart';
```

### 4. Otimize Imagens

```tsx
// ✅ Bom: Next.js Image
<Image src="/img.jpg" width={500} height={300} />

// ❌ Ruim: Tag img normal
<img src="/img.jpg" />
```

## Ferramentas de Análise

### Lighthouse

```bash
# Executar Lighthouse
npx lighthouse http://localhost:3000
```

### Bundle Analyzer

```bash
# Analisar bundle
npm run build
# Ver relatório em .next/analyze
```

## Checklist de Performance

Antes de fazer deploy:

- [ ] Bundle size < 500KB (gzipped)
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1
- [ ] Imagens otimizadas
- [ ] CSS minificado
- [ ] Code splitting implementado
- [ ] Lazy loading de componentes pesados

---

**Referência**: 
- [Next.js Performance](https://nextjs.org/docs/app/building-your-application/optimizing)
- [Web Vitals](https://web.dev/vitals/)
