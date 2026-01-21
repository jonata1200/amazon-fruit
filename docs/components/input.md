# 📝 Componente Input

## Visão Geral

O componente Input é usado para campos de entrada de texto, números e outros tipos de dados. Suporta estados de validação, ícones e diferentes tamanhos.

## Uso Básico

```tsx
import { Input } from '@/components/ui/input';

<Input placeholder="Digite aqui" />
```

## Tamanhos

### Small
```tsx
<Input size="sm" placeholder="Pequeno" />
```

### Medium (Padrão)
```tsx
<Input size="md" placeholder="Médio" />
```

### Large
```tsx
<Input size="lg" placeholder="Grande" />
```

## Estados

### Default
```tsx
<Input state="default" placeholder="Estado padrão" />
```

### Error
```tsx
<Input 
  state="error" 
  placeholder="Campo com erro"
  showStateIcon
/>
```

### Success
```tsx
<Input 
  state="success" 
  placeholder="Campo válido"
  showStateIcon
/>
```

### Warning
```tsx
<Input 
  state="warning" 
  placeholder="Aviso"
/>
```

### Disabled
```tsx
<Input disabled placeholder="Desabilitado" />
```

## Ícones

### Ícone à Esquerda
```tsx
import { Search } from 'lucide-react';

<Input 
  leftIcon={<Search className="h-4 w-4" />}
  placeholder="Buscar..."
/>
```

### Ícone à Direita
```tsx
import { Eye, EyeOff } from 'lucide-react';

<Input 
  type="password"
  rightIcon={<Eye className="h-4 w-4" />}
  placeholder="Senha"
/>
```

### Ícones de Estado Automáticos
```tsx
<Input 
  state="error"
  showStateIcon
  placeholder="Campo com erro"
  // Ícone de erro aparece automaticamente
/>
```

## Tipos de Input

### Text
```tsx
<Input type="text" placeholder="Texto" />
```

### Email
```tsx
<Input type="email" placeholder="email@exemplo.com" />
```

### Password
```tsx
<Input type="password" placeholder="Senha" />
```

### Number
```tsx
<Input type="number" placeholder="Número" />
```

### Date
```tsx
<Input type="date" />
```

## Acessibilidade

O componente inclui suporte ARIA automático:

```tsx
<Input 
  state="error"
  aria-invalid="true"
  aria-describedby="error-message"
/>
```

## Exemplos Completos

### Formulário com Validação
```tsx
function LoginForm() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState(false);

  return (
    <form>
      <Input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        state={error ? 'error' : 'default'}
        showStateIcon={error}
        placeholder="Email"
      />
      {error && (
        <p className="text-sm text-error-500 mt-1">
          Email inválido
        </p>
      )}
    </form>
  );
}
```

### Input com Label
```tsx
import { Label } from '@/components/ui/label';

<div className="space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input 
    id="email"
    type="email"
    placeholder="seu@email.com"
  />
</div>
```

## Props

| Prop | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | Tamanho do input |
| `state` | `'default' \| 'error' \| 'success' \| 'warning'` | `'default'` | Estado visual |
| `leftIcon` | `ReactNode` | - | Ícone à esquerda |
| `rightIcon` | `ReactNode` | - | Ícone à direita |
| `showStateIcon` | `boolean` | `false` | Mostrar ícone de estado automaticamente |
| `disabled` | `boolean` | `false` | Desabilitar input |
| `type` | `string` | `'text'` | Tipo do input HTML |

## Boas Práticas

1. **Use labels**: Sempre associe um label ao input
2. **Validação clara**: Use estados de erro/sucesso para feedback
3. **Placeholders úteis**: Use placeholders descritivos
4. **Acessibilidade**: Use `aria-describedby` para mensagens de erro
5. **Ícones contextuais**: Use ícones que ajudem a entender o campo

---

**Referência**: `src/components/ui/input.tsx`
