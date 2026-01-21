# 🌙 Guia de Dark Mode

## Visão Geral

O projeto suporta dark mode completo através de variáveis CSS e design tokens, garantindo uma experiência consistente em ambos os modos.

## Implementação

### Sistema de Cores

O dark mode é implementado usando variáveis CSS que mudam dinamicamente:

```css
:root {
  --background: 0 0% 100%;        /* Branco no modo claro */
  --foreground: 270 50% 20%;      /* Texto escuro */
}

.dark {
  --background: 270 40% 10%;      /* Fundo escuro */
  --foreground: 270 20% 95%;      /* Texto claro */
}
```

### Toggle de Dark Mode

```tsx
import { useColorMode } from '@/lib/hooks/use-color-mode';

function ThemeToggle() {
  const { theme, toggleTheme, isDark } = useColorMode();

  return (
    <button onClick={toggleTheme}>
      {isDark ? '☀️' : '🌙'}
    </button>
  );
}
```

## Design Tokens

### Cores

Todas as cores do design system suportam dark mode automaticamente através de variáveis CSS:

```tsx
// Cores que se adaptam automaticamente
<div className="bg-background text-foreground">
  {/* Adapta-se ao modo atual */}
</div>

<div className="bg-primary text-primary-foreground">
  {/* Cores semânticas também se adaptam */}
</div>
```

### Sombras

As sombras são ajustadas para dark mode:

```typescript
import { shadows, shadowsDark } from '@/lib/design-tokens';

// Modo claro
const lightShadow = shadows.md;

// Modo escuro (mais intenso)
const darkShadow = shadowsDark.md;
```

## Componentes

Todos os componentes do design system suportam dark mode automaticamente:

```tsx
// Botões
<Button variant="default">Ação</Button>

// Cards
<Card>Conteúdo</Card>

// Inputs
<Input placeholder="Digite aqui" />

// Todos se adaptam automaticamente ao modo atual
```

## Boas Práticas

### 1. Use Variáveis CSS

```tsx
// ✅ Bom: Usa variáveis CSS
<div className="bg-background text-foreground">

// ❌ Ruim: Cores hardcoded
<div className="bg-white text-black dark:bg-gray-900 dark:text-white">
```

### 2. Teste Contraste

Sempre teste o contraste em ambos os modos:

```typescript
import { meetsContrastRatio } from '@/lib/utils/colors';

// Validar contraste
const hasGoodContrast = meetsContrastRatio(
  foregroundColor,
  backgroundColor,
  'AA',
  'normal'
);
```

### 3. Considere Sombras

No dark mode, sombras podem precisar ser mais intensas:

```tsx
<div className="shadow-md dark:shadow-lg">
  {/* Sombra mais intensa no dark mode */}
</div>
```

### 4. Imagens e Ícones

Considere usar ícones e imagens que funcionem bem em ambos os modos:

```tsx
<Icon 
  className="text-foreground"
  // Ícone que se adapta à cor do texto
/>
```

## Transições

As transições entre modos são suaves:

```css
/* Transição automática em globals.css */
* {
  transition: background-color 200ms, color 200ms;
}
```

## Persistência

O tema é persistido no store (Zustand) e pode ser sincronizado com localStorage:

```typescript
// O store já gerencia a persistência
const { theme, setTheme } = useColorMode();
```

## Testes

### Testar em Ambos os Modos

```tsx
// Em testes
it('renders correctly in dark mode', () => {
  document.documentElement.classList.add('dark');
  render(<Component />);
  // Testes...
});
```

### Verificar Contraste

```typescript
// Validar contraste em ambos os modos
const lightContrast = meetsContrastRatio('#000', '#fff', 'AA');
const darkContrast = meetsContrastRatio('#fff', '#000', 'AA');
```

## Troubleshooting

### Cores não mudam no dark mode

1. Verifique se está usando variáveis CSS (`bg-background` ao invés de `bg-white`)
2. Confirme que a classe `dark` está aplicada no elemento raiz
3. Verifique se as variáveis CSS estão definidas corretamente

### Contraste insuficiente

1. Use `meetsContrastRatio` para validar
2. Ajuste as cores nas variáveis CSS se necessário
3. Considere usar cores mais contrastantes

### Transições não suaves

1. Verifique se `transition-all` está aplicado
2. Confirme que as durações estão configuradas
3. Teste com `prefers-reduced-motion` desabilitado

---

**Referência**: 
- `src/lib/hooks/use-color-mode.ts`
- `src/app/globals.css`
- `src/lib/design-tokens/colors.ts`
