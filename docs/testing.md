# 🧪 Guia de Testes

## Visão Geral

Este projeto usa **Jest** com **React Testing Library** para testes unitários de componentes, hooks e utilitários.

## Estrutura

```
tests/
├── unit/              # Testes unitários
│   ├── components/   # Componentes
│   ├── lib/         # Hooks e utilitários
│   └── store/       # Store (Zustand)
├── helpers/         # Utilitários de teste
└── templates/       # Templates para novos testes
```

## Executando Testes

```bash
# Todos os testes
npm test

# Modo watch (desenvolvimento)
npm run test:watch

# Com cobertura
npm run test:coverage

# Teste específico
npm test button.test.tsx
npm test -- --testNamePattern="Button"
```

## Escrevendo Testes

### Estrutura Básica

```tsx
import { render, screen } from '@testing-library/react';
import { Button } from '@/components/ui/button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
});
```

### Padrão AAA

```tsx
it('handles click', async () => {
  // Arrange
  const handleClick = jest.fn();
  const user = userEvent.setup();

  // Act
  render(<Button onClick={handleClick}>Click</Button>);
  await user.click(screen.getByText('Click'));

  // Assert
  expect(handleClick).toHaveBeenCalled();
});
```

### Testando Componentes

```tsx
// Renderização
it('renders with text', () => {
  render(<Button>Click</Button>);
  expect(screen.getByText('Click')).toBeInTheDocument();
});

// Props
it('applies variant', () => {
  render(<Button variant="destructive">Delete</Button>);
  expect(screen.getByText('Delete').className).toContain('destructive');
});

// Interações
it('handles click', async () => {
  const handleClick = jest.fn();
  const user = userEvent.setup();
  render(<Button onClick={handleClick}>Click</Button>);
  await user.click(screen.getByText('Click'));
  expect(handleClick).toHaveBeenCalled();
});

// Estados
it('handles disabled', () => {
  render(<Button disabled>Disabled</Button>);
  expect(screen.getByText('Disabled')).toBeDisabled();
});
```

### Testando Hooks

```tsx
import { renderHook, act } from '@testing-library/react';
import { useDebounce } from '@/lib/hooks/useDebounce';

it('debounces value', async () => {
  const { result, rerender } = renderHook(
    ({ value }) => useDebounce(value, 300),
    { initialProps: { value: 'initial' } }
  );
  
  expect(result.current).toBe('initial');
  rerender({ value: 'updated' });
  
  await act(async () => {
    await new Promise(resolve => setTimeout(resolve, 300));
  });
  
  expect(result.current).toBe('updated');
});
```

### Helpers Customizados

```tsx
// Para componentes com React Query
import { renderWithProviders } from '@/tests/helpers/test-utils';

renderWithProviders(<Component />);

// Mock data
import { mockDashboardGeralData } from '@/tests/helpers/test-utils';
```

## Queries (Prioridade)

1. `getByRole` - Mais acessível
2. `getByLabelText` - Para inputs
3. `getByPlaceholderText` - Placeholders
4. `getByText` - Texto visível
5. `getByTestId` - Último recurso

```tsx
// getBy - lança erro se não encontrar
screen.getByRole('button');

// queryBy - retorna null
const button = screen.queryByRole('button');
expect(button).not.toBeInTheDocument();

// findBy - aguarda elemento (assíncrono)
const button = await screen.findByRole('button');
```

## Matchers Úteis

```tsx
expect(element).toBeInTheDocument();
expect(element).toBeVisible();
expect(button).toBeDisabled();
expect(input).toHaveValue('text');
expect(element).toHaveClass('active');
expect(element).toHaveTextContent('Hello');
```

## Cobertura

Threshold mínimo: **50%** (branches, functions, lines, statements)

```bash
npm run test:coverage
# Abre: coverage/index.html
```

## Criando Novos Testes

Use os templates:

```bash
# Componente
cp tests/templates/component.test.template.tsx tests/unit/components/ui/meu-componente.test.tsx

# Hook
cp tests/templates/hook.test.template.ts tests/unit/lib/hooks/meu-hook.test.ts
```

## Boas Práticas

### ✅ Fazer
- Teste **comportamento**, não implementação
- Use `getByRole` quando possível
- Mantenha testes **isolados** e **independentes**
- Use nomes **descritivos**
- Siga padrão **AAA** (Arrange-Act-Assert)

### ❌ Evitar
- Testar detalhes de implementação
- Usar `container.querySelector`
- Testes muito específicos (fragilidade)
- Ignorar testes que falham
- Testar bibliotecas externas

## Debugging

```tsx
import { debug, logRoles } from '@testing-library/react';

// Ver HTML renderizado
debug();

// Ver roles disponíveis
logRoles(screen.getByTestId('container'));

// Pausar teste
debugger;
```

## Troubleshooting

**"Cannot find module"**: Verifique path mapping `@/`

**"act(...) is not defined"**: Use `act` do `@testing-library/react`

**Testes lentos**: Use `--runInBand` ou `jest.useFakeTimers()`

## Recursos

- [Jest Docs](https://jestjs.io/docs/getting-started)
- [React Testing Library](https://testing-library.com/react)
- Templates: `tests/templates/`
- Exemplos: `tests/unit/`

---

**Checklist antes de commit:**
- [ ] Todos os testes passam
- [ ] Coverage ≥ 50%
- [ ] Testes isolados e rápidos
- [ ] Nomes descritivos
- [ ] Edge cases cobertos
