# 🧪 Guia de Testes - Amazon Fruit

Este documento descreve a estratégia de testes, estrutura e padrões para escrever testes no projeto Amazon Fruit.

## 📁 Estrutura de Testes

```
tests/
├── unit/                    # Testes unitários
│   ├── components/
│   │   ├── ui/             # Testes de componentes UI
│   │   ├── features/        # Testes de features
│   │   ├── dashboards/      # Testes de dashboards
│   │   └── charts/          # Testes de gráficos
│   ├── lib/
│   │   ├── hooks/           # Testes de hooks customizados
│   │   ├── utils/           # Testes de utilitários
│   │   └── api/             # Testes de API
│   └── store/               # Testes do store Zustand
├── integration/             # Testes de integração
├── e2e/                     # Testes end-to-end (Playwright)
└── helpers/                 # Helpers compartilhados
    ├── test-utils.tsx       # Utilitários de teste
    └── mocks/               # Mocks compartilhados
```

## 🎯 Estratégia de Testes

### Testes Unitários
Testam componentes, hooks e utilitários de forma isolada.

**Localização:** `tests/unit/`

**Exemplo:**
```typescript
// tests/unit/components/ui/button.test.tsx
import { render, screen } from '@testing-library/react';
import { Button } from '@/components/ui/button';

describe('Button', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
});
```

### Testes de Integração
Testam múltiplos componentes trabalhando juntos.

**Localização:** `tests/integration/`

### Testes E2E
Testam fluxos completos da aplicação.

**Localização:** `tests/e2e/`

## 📝 Convenções de Nomenclatura

- **Arquivos de teste:** `*.test.ts` ou `*.test.tsx`
- **Descreva o que está sendo testado:** Use `describe` para agrupar testes relacionados
- **Testes descritivos:** Use `it('should ...')` ou `it('renders ...')` para descrever o comportamento

## 🛠️ Ferramentas

### Jest
Framework de testes principal.

### Testing Library
- `@testing-library/react` - Para testar componentes React
- `@testing-library/user-event` - Para simular interações do usuário
- `@testing-library/jest-dom` - Matchers adicionais para DOM

### Helpers
Use `renderWithProviders` de `tests/helpers/test-utils.tsx` para renderizar componentes com providers necessários:

```typescript
import { renderWithProviders } from '@/tests/helpers/test-utils';

renderWithProviders(<MyComponent />);
```

## 📋 Padrões de Teste

### Estrutura AAA (Arrange-Act-Assert)

```typescript
it('should do something', () => {
  // Arrange: Preparar o teste
  const props = { title: 'Test' };
  
  // Act: Executar a ação
  render(<Component {...props} />);
  
  // Assert: Verificar o resultado
  expect(screen.getByText('Test')).toBeInTheDocument();
});
```

### Testando Componentes

```typescript
describe('ComponentName', () => {
  it('renders correctly', () => {
    // Teste básico de renderização
  });

  it('handles user interactions', () => {
    // Teste de interações
  });

  it('applies props correctly', () => {
    // Teste de props
  });
});
```

### Testando Hooks

```typescript
import { renderHook, act } from '@testing-library/react';

describe('useCustomHook', () => {
  it('returns initial value', () => {
    const { result } = renderHook(() => useCustomHook());
    expect(result.current.value).toBe(initialValue);
  });

  it('updates value on action', () => {
    const { result } = renderHook(() => useCustomHook());
    
    act(() => {
      result.current.updateValue('new');
    });
    
    expect(result.current.value).toBe('new');
  });
});
```

## 🎨 Mocks

### Mock de Módulos

```typescript
jest.mock('@/store', () => ({
  useAppStore: jest.fn(),
}));
```

### Mock de Hooks

```typescript
jest.mock('@/lib/hooks/useAlerts', () => ({
  useAlerts: jest.fn(() => ({
    data: { alerts: [] },
    isLoading: false,
  })),
}));
```

## ✅ Boas Práticas

1. **Teste comportamento, não implementação**
   - ✅ Teste o que o usuário vê/faz
   - ❌ Não teste detalhes internos

2. **Mantenha testes simples e focados**
   - Um teste = um comportamento

3. **Use nomes descritivos**
   - `it('should display error message when API fails')`
   - Não: `it('test1')`

4. **Evite testes frágeis**
   - Não dependa de ordem de execução
   - Use dados de teste isolados

5. **Teste casos de borda**
   - Valores vazios
   - Estados de erro
   - Estados de loading

## 🚀 Executando Testes

```bash
# Todos os testes
npm test

# Modo watch
npm test -- --watch

# Com cobertura
npm test -- --coverage

# Apenas testes unitários
npm test -- tests/unit

# Arquivo específico
npm test -- button.test.tsx
```

## 🔍 Troubleshooting

### Teste falha com "Unable to find element"
- Verifique se o componente está renderizando corretamente
- Use `screen.debug()` para ver o DOM renderizado
- Verifique se há condições que impedem a renderização
- Confirme que está usando o seletor correto (role, text, etc.)

### Erro de "act()"
- Envolva atualizações de estado com `waitFor()`
- Use `userEvent` em vez de `fireEvent` quando possível
- Certifique-se de aguardar operações assíncronas

### Mock não funciona
- Verifique se o mock está antes do import
- Use `jest.clearAllMocks()` no `beforeEach`
- Verifique a ordem dos mocks
- Use `jest.resetModules()` se necessário

### Teste é instável (flaky)
- Evite dependências de tempo (use `jest.useFakeTimers()`)
- Isole testes uns dos outros
- Evite dependências de ordem de execução
- Use `waitFor` com timeout apropriado

### Cobertura não está sendo coletada
- Verifique `collectCoverageFrom` no `jest.config.js`
- Confirme que os arquivos não estão na lista de exclusões
- Execute `npm test -- --coverage` explicitamente

## 📋 Checklist para Code Review de Testes

Ao revisar testes em PRs, verifique:

- [ ] Testes seguem o padrão AAA (Arrange-Act-Assert)
- [ ] Nomes de testes são descritivos
- [ ] Testes são independentes (não dependem de outros)
- [ ] Mocks são apropriados e não excessivos
- [ ] Casos de borda são cobertos
- [ ] Testes de acessibilidade quando aplicável
- [ ] Não há testes duplicados ou redundantes
- [ ] Testes são rápidos (< 1s cada)
- [ ] Cobertura não diminuiu significativamente

## 🎯 Metas de Cobertura

- **Componentes UI:** 80%+
- **Hooks:** 85%+
- **Utilitários:** 90%+
- **Features:** 75%+
- **Dashboards:** 70%+

## 📚 Recursos

- [Testing Library Docs](https://testing-library.com/)
- [Jest Docs](https://jestjs.io/)
- [Plano de Implementação](./plano-implementacao-teste-overview.md)
- [Guia de Testes de Integração](./testes-integracao.md)
- [Templates de Teste](../tests/templates/)

---

**Última atualização:** 2024
