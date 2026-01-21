# ♿ Guia de Acessibilidade

## Visão Geral

Este guia documenta padrões de acessibilidade do design system, garantindo conformidade com WCAG 2.1.

## Checklist de Acessibilidade

### Contraste de Cores
- ✅ Texto normal: mínimo 4.5:1
- ✅ Texto grande: mínimo 3:1
- ✅ Componentes interativos: mínimo 3:1

### Navegação por Teclado
- ✅ Todos os elementos interativos são focáveis
- ✅ Ordem de tabulação lógica
- ✅ Focus visível em todos os elementos
- ✅ Atalhos de teclado documentados

### ARIA
- ✅ Labels descritivos
- ✅ Estados comunicados (aria-expanded, aria-busy)
- ✅ Landmarks semânticos
- ✅ Roles apropriados

### Semântica HTML
- ✅ Tags HTML corretas (button, nav, main, etc)
- ✅ Hierarquia de cabeçalhos (h1-h6)
- ✅ Listas estruturadas (ul, ol)
- ✅ Formulários acessíveis (label, fieldset)

## Helpers de Acessibilidade

### Gerar ID Único
```typescript
import { generateId } from '@/lib/utils';

const id = generateId('button'); // 'button-abc123'
```

### Criar Atributos ARIA
```typescript
import { createAriaAttributes } from '@/lib/utils';

const ariaAttrs = createAriaAttributes({
  label: 'Fechar diálogo',
  expanded: true,
  busy: false,
});
```

### Screen Reader Only
```typescript
import { srOnly } from '@/lib/utils';

<span {...srOnly('Texto apenas para leitores de tela')} />
```

### Handlers de Teclado
```typescript
import { createKeyboardHandlers } from '@/lib/utils';

const handlers = createKeyboardHandlers({
  onEnter: () => handleSubmit(),
  onEscape: () => handleClose(),
});
```

## Verificar Contraste

```typescript
import { meetsContrastRatio } from '@/lib/utils';

const isValid = meetsContrastRatio(
  '#000000',  // foreground
  '#ffffff',  // background
  'AA',       // nível WCAG
  'normal'    // tamanho do texto
);
```

## Padrões por Componente

### Botões
```tsx
<Button
  aria-label="Fechar diálogo"
  aria-busy={loading}
  disabled={disabled}
>
  Fechar
</Button>
```

### Inputs
```tsx
<Input
  aria-label="Nome completo"
  aria-invalid={hasError}
  aria-describedby={errorId}
/>
{error && (
  <span id={errorId} role="alert">
    {error}
  </span>
)}
```

### Dialogs
```tsx
<Dialog
  aria-labelledby="dialog-title"
  aria-describedby="dialog-description"
>
  <DialogTitle id="dialog-title">Título</DialogTitle>
  <DialogDescription id="dialog-description">
    Descrição
  </DialogDescription>
</Dialog>
```

## Testes de Acessibilidade

### Ferramentas Recomendadas
- **axe DevTools**: Extensão do navegador
- **WAVE**: Avaliação web
- **Lighthouse**: Auditoria do Chrome
- **NVDA/JAWS**: Leitores de tela

### Checklist de Teste
1. ✅ Navegar apenas com teclado
2. ✅ Testar com leitor de tela
3. ✅ Verificar contraste de cores
4. ✅ Validar HTML semântico
5. ✅ Testar em diferentes tamanhos de fonte

## Boas Práticas

1. **Sempre forneça labels** para elementos interativos
2. **Use HTML semântico** ao invés de divs genéricas
3. **Teste com leitores de tela** regularmente
4. **Mantenha foco visível** em todos os elementos
5. **Comunique mudanças de estado** via ARIA

## Recursos

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
