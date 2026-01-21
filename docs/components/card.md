# 🃏 Componente Card

## Visão Geral

O componente Card é usado para agrupar conteúdo relacionado em um container visualmente destacado. Suporta diferentes variantes de elevação e padding.

## Uso Básico

```tsx
import { Card, CardContent } from '@/components/ui/card';

<Card>
  <CardContent>
    Conteúdo do card
  </CardContent>
</Card>
```

## Variantes

### Default
```tsx
<Card variant="default">
  <CardContent>Card padrão com sombra sutil</CardContent>
</Card>
```

### Outlined
```tsx
<Card variant="outlined">
  <CardContent>Card apenas com borda, sem sombra</CardContent>
</Card>
```

### Elevated
```tsx
<Card variant="elevated">
  <CardContent>Card com sombra mais pronunciada</CardContent>
</Card>
```

### Filled
```tsx
<Card variant="filled">
  <CardContent>Card com fundo preenchido</CardContent>
</Card>
```

## Padding

### None
```tsx
<Card padding="none">
  <CardContent>Sem padding interno</CardContent>
</Card>
```

### Small
```tsx
<Card padding="sm">
  <CardContent>Padding pequeno (16px)</CardContent>
</Card>
```

### Medium (Padrão)
```tsx
<Card padding="md">
  <CardContent>Padding médio (24px)</CardContent>
</Card>
```

### Large
```tsx
<Card padding="lg">
  <CardContent>Padding grande (32px)</CardContent>
</Card>
```

## Estrutura Completa

### Com Header e Footer
```tsx
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from '@/components/ui/card';

<Card>
  <CardHeader>
    <CardTitle>Título do Card</CardTitle>
    <CardDescription>Descrição do card</CardDescription>
  </CardHeader>
  <CardContent>
    Conteúdo principal do card
  </CardContent>
  <CardFooter>
    <Button>Ação</Button>
  </CardFooter>
</Card>
```

## Exemplos

### Card Simples
```tsx
<Card>
  <CardContent className="p-6">
    <h3 className="text-lg font-semibold mb-2">Título</h3>
    <p className="text-muted-foreground">
      Descrição do conteúdo
    </p>
  </CardContent>
</Card>
```

### Card com Hover
```tsx
<Card className="hover:shadow-md transition-shadow">
  <CardContent>
    Card que eleva ao passar o mouse
  </CardContent>
</Card>
```

### Card de Produto
```tsx
<Card variant="elevated">
  <CardHeader>
    <CardTitle>Produto</CardTitle>
    <CardDescription>R$ 99,90</CardDescription>
  </CardHeader>
  <CardContent>
    <img src="/product.jpg" alt="Produto" />
  </CardContent>
  <CardFooter>
    <Button className="w-full">Comprar</Button>
  </CardFooter>
</Card>
```

### Grid de Cards
```tsx
<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
  <Card>
    <CardContent>Card 1</CardContent>
  </Card>
  <Card>
    <CardContent>Card 2</CardContent>
  </Card>
  <Card>
    <CardContent>Card 3</CardContent>
  </Card>
</div>
```

## Sub-componentes

### CardHeader
Container para título e descrição:

```tsx
<CardHeader>
  <CardTitle>Título</CardTitle>
  <CardDescription>Descrição</CardDescription>
</CardHeader>
```

### CardTitle
Título do card (h3):

```tsx
<CardTitle>Título do Card</CardTitle>
```

### CardDescription
Descrição do card:

```tsx
<CardDescription>Texto descritivo</CardDescription>
```

### CardContent
Conteúdo principal:

```tsx
<CardContent>
  Conteúdo aqui
</CardContent>
```

### CardFooter
Rodapé do card:

```tsx
<CardFooter>
  <Button>Ação</Button>
</CardFooter>
```

## Props

| Prop | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `variant` | `'default' \| 'outlined' \| 'elevated' \| 'filled'` | `'default'` | Variante visual |
| `padding` | `'none' \| 'sm' \| 'md' \| 'lg'` | `'md'` | Padding interno |

## Boas Práticas

1. **Use variantes apropriadas**: `elevated` para destaque, `outlined` para conteúdo secundário
2. **Mantenha consistência**: Use o mesmo padding em cards similares
3. **Estrutura clara**: Use sub-componentes para organização
4. **Hover states**: Adicione transições suaves em hover quando relevante
5. **Acessibilidade**: Use headings semânticos no CardTitle

---

**Referência**: `src/components/ui/card.tsx`
