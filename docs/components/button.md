# 🔘 Componente Button

## Visão Geral

O componente Button é usado para ações principais e secundárias na interface.

## Uso Básico

```tsx
import { Button } from '@/components/ui/button';

<Button>Clique aqui</Button>
```

## Variantes

### Default (Primário)
```tsx
<Button variant="default">Salvar</Button>
```

### Destructive
```tsx
<Button variant="destructive">Excluir</Button>
```

### Outline
```tsx
<Button variant="outline">Cancelar</Button>
```

### Secondary
```tsx
<Button variant="secondary">Secundário</Button>
```

### Ghost
```tsx
<Button variant="ghost">Ação discreta</Button>
```

### Link
```tsx
<Button variant="link">Link como botão</Button>
```

### Success / Warning
```tsx
<Button variant="success">Confirmar</Button>
<Button variant="warning">Avisar</Button>
```

## Tamanhos

```tsx
<Button size="xs">Extra pequeno</Button>
<Button size="sm">Pequeno</Button>
<Button size="md">Médio (padrão)</Button>
<Button size="lg">Grande</Button>
<Button size="xl">Extra grande</Button>
<Button size="icon">Ícone</Button>
```

## Estados

### Loading
```tsx
<Button loading>Carregando...</Button>
```

### Disabled
```tsx
<Button disabled>Desabilitado</Button>
```

## Com Ícones

```tsx
import { Save, Trash2 } from 'lucide-react';

<Button leftIcon={<Save />}>Salvar</Button>
<Button rightIcon={<Trash2 />}>Excluir</Button>
<Button size="icon" leftIcon={<Save />} />
```

## Props

| Prop | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `variant` | `'default' \| 'destructive' \| 'outline' \| 'secondary' \| 'ghost' \| 'link' \| 'success' \| 'warning'` | `'default'` | Variante visual |
| `size` | `'xs' \| 'sm' \| 'md' \| 'lg' \| 'xl' \| 'icon'` | `'md'` | Tamanho do botão |
| `loading` | `boolean` | `false` | Mostra estado de carregamento |
| `disabled` | `boolean` | `false` | Desabilita o botão |
| `leftIcon` | `ReactNode` | - | Ícone à esquerda |
| `rightIcon` | `ReactNode` | - | Ícone à direita |
| `asChild` | `boolean` | `false` | Renderiza como child |

## Acessibilidade

- Suporta `aria-disabled` e `aria-busy`
- Navegação por teclado (Enter, Space)
- Focus visible configurado
- Contraste adequado em todas as variantes

## Exemplos Completos

```tsx
// Botão primário com loading
<Button variant="default" loading>
  Salvar alterações
</Button>

// Botão com ícone e ação
<Button 
  variant="destructive" 
  leftIcon={<Trash2 />}
  onClick={handleDelete}
>
  Excluir item
</Button>

// Botão desabilitado
<Button disabled={!isValid}>
  Enviar formulário
</Button>
```

## Boas Práticas

1. **Use variant="default"** para ações primárias
2. **Use variant="destructive"** apenas para ações destrutivas
3. **Mantenha labels descritivos** ("Salvar" ao invés de "OK")
4. **Use loading state** para ações assíncronas
5. **Desabilite botões** quando a ação não é possível

## Anti-patterns

```tsx
// ❌ Ruim: Múltiplos botões primários
<Button variant="default">Salvar</Button>
<Button variant="default">Cancelar</Button>

// ✅ Bom: Um primário, outros secundários
<Button variant="default">Salvar</Button>
<Button variant="outline">Cancelar</Button>

// ❌ Ruim: Label vago
<Button>Clique</Button>

// ✅ Bom: Label descritivo
<Button>Salvar alterações</Button>
```
