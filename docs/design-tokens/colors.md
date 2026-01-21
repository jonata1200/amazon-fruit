# 🎨 Design Tokens - Cores

## Visão Geral

O sistema de cores do design system é baseado em uma paleta semântica que garante consistência, acessibilidade e suporte a dark mode.

## Estrutura

As cores são organizadas em:
- **Cores Semânticas**: primary, secondary, success, warning, error, info
- **Cores Neutras**: neutral (escala de cinzas)
- **Cores de Estado**: stateColors (hover, active, disabled, etc)
- **Opacidade**: valores pré-definidos de opacidade

## Cores Semânticas

### Primary (Roxo)
Cor principal do sistema, usada para ações primárias e elementos de destaque.

| Escala | Hex | Uso |
|--------|-----|-----|
| 50 | `#faf5ff` | Backgrounds muito claros |
| 100 | `#f3e8ff` | Backgrounds claros |
| 200 | `#e9d5ff` | Borders claros |
| 300 | `#d8b4fe` | Hover states |
| 400 | `#c084fc` | Secondary actions |
| 500 | `#a855f7` | Base color |
| **600** | `#9333ea` | **Cor principal** |
| 700 | `#7e22ce` | Hover states escuros |
| 800 | `#6b21a8` | Active states |
| 900 | `#581c87` | Texto em backgrounds claros |
| 950 | `#3b0764` | Texto em backgrounds muito claros |

### Secondary (Cinza Azulado)
Cor secundária, usada para elementos de apoio e backgrounds.

### Success (Verde)
Usada para indicar sucesso, confirmações e estados positivos.

### Warning (Amarelo/Laranja)
Usada para alertas e avisos.

### Error (Vermelho)
Usada para erros, validações negativas e ações destrutivas.

### Info (Azul)
Usada para informações e notificações.

## Uso em Tailwind

```tsx
// Classes Tailwind
<div className="bg-primary-600 text-primary-50">
  Botão primário
</div>

// Com opacidade
<div className="bg-primary-600/50">
  Background com opacidade
</div>

// Dark mode automático
<div className="bg-primary dark:bg-primary-700">
  Adapta automaticamente
</div>
```

## Uso em JavaScript/TypeScript

```typescript
import { getColor, getColorWithOpacity } from '@/lib/utils';

// Obter cor
const primaryColor = getColor('primary', 600); // '#9333ea'

// Obter cor com opacidade
const primaryWithOpacity = getColorWithOpacity('primary', 600, 0.5);
```

## Cores Semânticas do Tailwind

O sistema também define cores semânticas que funcionam com dark mode:

- `bg-primary` / `text-primary-foreground`
- `bg-secondary` / `text-secondary-foreground`
- `bg-destructive` / `text-destructive-foreground`
- `bg-muted` / `text-muted-foreground`
- `bg-accent` / `text-accent-foreground`

## Acessibilidade

Todas as cores foram testadas para garantir contraste WCAG AA:
- Texto normal: mínimo 4.5:1
- Texto grande: mínimo 3:1

Use `meetsContrastRatio()` para validar contraste:

```typescript
import { meetsContrastRatio } from '@/lib/utils';

const isValid = meetsContrastRatio('#000', '#fff', 'AA', 'normal');
```

## Dark Mode

As cores se adaptam automaticamente ao dark mode através de variáveis CSS:

```css
:root {
  --primary: 270 60% 55%;
}

.dark {
  --primary: 270 65% 65%;
}
```

## Referência Rápida

| Token | Tailwind Class | Uso |
|-------|----------------|-----|
| `primary.600` | `bg-primary-600` | Cor principal |
| `success.600` | `bg-success-600` | Sucesso |
| `error.600` | `bg-error-600` | Erro |
| `warning.600` | `bg-warning-600` | Aviso |
| `info.600` | `bg-info-600` | Informação |

## Boas Práticas

1. **Use cores semânticas** ao invés de cores hardcoded
2. **Prefira escalas 500-700** para elementos interativos
3. **Use opacidade** para criar variações sutis
4. **Teste contraste** antes de usar cores em texto
5. **Respeite dark mode** usando variáveis CSS

## Exemplos

```tsx
// ✅ Bom: Usando tokens
<Button className="bg-primary-600 hover:bg-primary-700" />

// ❌ Ruim: Cor hardcoded
<Button className="bg-[#9333ea]" />

// ✅ Bom: Com opacidade
<div className="bg-primary-600/10" />

// ✅ Bom: Semântico
<Button variant="destructive" />
```
