# 📚 Guia de Testes de Integração

Este documento descreve como escrever e executar testes de integração no projeto Amazon Fruit.

## 📁 Estrutura

Os testes de integração estão organizados em `tests/integration/`:

```
tests/integration/
├── components/      # Testes de integração de componentes UI
├── features/        # Testes de integração de features
├── dashboards/      # Testes de integração de dashboards
├── flows/           # Testes de fluxos completos
├── helpers/         # Helpers e utilitários para testes
└── mocks/           # Mocks compartilhados
```

## 🛠️ Helpers Disponíveis

### `renderWithProviders`

Renderiza componentes com todos os providers necessários (QueryClient, Theme, etc.):

```tsx
import { renderWithProviders, screen } from '../helpers/render-with-providers';

test('exemplo', () => {
  renderWithProviders(<MeuComponente />);
  expect(screen.getByText('Texto')).toBeInTheDocument();
});
```

### `mock-store.ts`

Utilitários para manipular o store Zustand:

```tsx
import { resetStore, setStoreState } from '../helpers/mock-store';

beforeEach(() => {
  resetStore(); // Reset para estado padrão
  setStoreState({ theme: 'dark' }); // Configurar estado específico
});
```

### `mock-api.ts`

Mocks para serviços de API:

```tsx
import { setupApiMocks, resetApiMocks, mockAlertsResponse } from '../helpers/mock-api';

beforeEach(() => {
  setupApiMocks();
  // Configurar retornos específicos
  mockAlertService.getAlerts.mockResolvedValue(mockAlertsResponse);
});
```

## 📝 Padrões de Teste

### 1. Estrutura Básica

```tsx
import { renderWithProviders, screen, waitFor } from '../helpers/render-with-providers';
import userEvent from '@testing-library/user-event';
import { MeuComponente } from '@/components/meu-componente';

describe('MeuComponente - Integração', () => {
  beforeEach(() => {
    // Setup
  });

  it('deve fazer algo', async () => {
    renderWithProviders(<MeuComponente />);
    // Testes
  });
});
```

### 2. Testando Interações

```tsx
it('deve responder a cliques', async () => {
  renderWithProviders(<MeuComponente />);
  
  const button = screen.getByRole('button', { name: 'Clique aqui' });
  await userEvent.click(button);
  
  await waitFor(() => {
    expect(screen.getByText('Resultado')).toBeInTheDocument();
  });
});
```

### 3. Testando Estado Global

```tsx
import { useAppStore } from '@/store';

it('deve atualizar o store', async () => {
  renderWithProviders(<MeuComponente />);
  
  // Interagir com componente
  await userEvent.click(screen.getByRole('button'));
  
  // Verificar store
  await waitFor(() => {
    expect(useAppStore.getState().algumEstado).toBe('valor');
  });
});
```

### 4. Testando Hooks Customizados

```tsx
// Mock do hook
jest.mock('@/lib/hooks/useMeuHook');
const mockUseMeuHook = useMeuHook as jest.MockedFunction<typeof useMeuHook>;

it('deve usar hook corretamente', () => {
  mockUseMeuHook.mockReturnValue({
    data: mockData,
    isLoading: false,
  });
  
  renderWithProviders(<MeuComponente />);
  // Testes
});
```

## 🎯 Boas Práticas

1. **Sempre resetar estado**: Use `resetStore()` no `beforeEach`
2. **Aguardar assíncrono**: Use `waitFor()` para operações assíncronas
3. **Mockar dependências externas**: APIs, navegação, etc.
4. **Testar comportamento, não implementação**: Foque no que o usuário vê/faz
5. **Manter testes independentes**: Cada teste deve poder rodar isoladamente

## 🚀 Executando Testes

```bash
# Todos os testes de integração
npm run test:integration

# Modo watch
npm run test:integration:watch

# Com cobertura
npm run test:integration:coverage

# Teste específico
npm test tests/integration/features/global-search.test.tsx
```

## 🔍 Troubleshooting

### Teste falha com "Unable to find element"

- Verifique se o componente está renderizando corretamente
- Use `screen.debug()` para ver o DOM renderizado
- Verifique se há condições que impedem a renderização

### Erro de "act()"

- Envolva atualizações de estado com `waitFor()`
- Use `userEvent` em vez de `fireEvent` quando possível

### Mock não funciona

- Verifique se o mock está antes do import
- Use `jest.clearAllMocks()` no `beforeEach`
- Verifique a ordem dos mocks

## 📚 Exemplos

Veja os testes existentes em `tests/integration/` para exemplos práticos:
- `features/global-search.test.tsx` - Busca global completa
- `features/alerts-system.test.tsx` - Sistema de alertas
- `flows/navigation-flow.test.tsx` - Fluxo de navegação
