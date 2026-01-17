# 🔧 Troubleshooting de Testes

Guia de resolução de problemas comuns em testes.

## Problemas Comuns

### 1. "Unable to find element"

**Sintoma:** Teste falha com erro "Unable to find an element with..."

**Soluções:**
```typescript
// ❌ Errado - pode não encontrar
expect(screen.getByText('Texto')).toBeInTheDocument();

// ✅ Correto - mais flexível
expect(screen.getByText(/texto/i)).toBeInTheDocument();

// ✅ Ou use debug para ver o DOM
screen.debug();
```

**Causas comuns:**
- Componente não renderizou completamente
- Texto está em elemento diferente
- Condição impede renderização
- Timing issue (componente ainda carregando)

### 2. Erro de "act()"

**Sintoma:** Warning "An update to Component inside a test was not wrapped in act(...)"

**Soluções:**
```typescript
// ❌ Errado
fireEvent.click(button);

// ✅ Correto - userEvent já envolve em act()
await userEvent.click(button);

// ✅ Ou use waitFor
await waitFor(() => {
  expect(screen.getByText('Result')).toBeInTheDocument();
});
```

### 3. Mock não funciona

**Sintoma:** Mock não está sendo aplicado

**Soluções:**
```typescript
// ✅ Mock antes do import
jest.mock('@/lib/api/services', () => ({
  alertService: {
    getAlerts: jest.fn(),
  },
}));

// Importar depois do mock
import { alertService } from '@/lib/api/services';

// Limpar mocks no beforeEach
beforeEach(() => {
  jest.clearAllMocks();
});
```

### 4. Teste instável (flaky)

**Sintoma:** Teste passa às vezes e falha outras

**Soluções:**
```typescript
// ✅ Usar waitFor com timeout
await waitFor(() => {
  expect(screen.getByText('Result')).toBeInTheDocument();
}, { timeout: 3000 });

// ✅ Evitar dependências de tempo
jest.useFakeTimers();
// ... teste
jest.useRealTimers();

// ✅ Isolar testes
beforeEach(() => {
  // Reset completo do estado
});
```

### 5. Cobertura não coletada

**Sintoma:** Arquivos não aparecem no relatório de cobertura

**Soluções:**
1. Verifique `collectCoverageFrom` no `jest.config.js`
2. Confirme que arquivos não estão excluídos
3. Execute explicitamente: `npm test -- --coverage`

### 6. Testes lentos

**Sintoma:** Suite de testes demora muito para executar

**Otimizações:**
```typescript
// ✅ Usar mocks em vez de implementações reais
jest.mock('heavy-library');

// ✅ Paralelizar quando possível
// Jest já faz isso por padrão

// ✅ Reduzir setup/teardown
beforeAll(() => {
  // Setup uma vez
});

afterAll(() => {
  // Cleanup uma vez
});
```

### 7. Erro de importação

**Sintoma:** "Cannot find module" ou erros de TypeScript

**Soluções:**
```typescript
// ✅ Verificar paths no jest.config.js
moduleNameMapper: {
  '^@/(.*)$': '<rootDir>/src/$1',
}

// ✅ Verificar tsconfig.json
// ✅ Verificar se arquivo existe
```

### 8. Estado compartilhado entre testes

**Sintoma:** Testes afetam uns aos outros

**Soluções:**
```typescript
// ✅ Sempre resetar no beforeEach
beforeEach(() => {
  jest.clearAllMocks();
  resetStore();
  // Reset qualquer estado global
});

// ✅ Usar dados isolados
const mockData = { ...baseMockData };
```

## Debug de Testes

### Usar screen.debug()

```typescript
it('debug example', () => {
  render(<Component />);
  screen.debug(); // Mostra todo o DOM
  screen.debug(screen.getByRole('button')); // Mostra apenas o botão
});
```

### Usar --verbose

```bash
npm test -- --verbose
```

### Executar teste específico

```bash
npm test -- ComponentName.test.tsx
```

### Executar com --no-coverage (mais rápido)

```bash
npm test -- --no-coverage
```

## Ferramentas Úteis

- **Jest Debugger:** Use breakpoints no VS Code
- **Testing Playground:** https://testing-playground.com/
- **React Testing Library Cheatsheet:** https://testing-library.com/docs/react-testing-library/cheatsheet/

## Quando Pedir Ajuda

Se você tentou as soluções acima e ainda tem problemas:

1. Verifique a documentação oficial
2. Procure issues similares no GitHub
3. Peça ajuda no time com:
   - Código do teste
   - Mensagem de erro completa
   - Stack trace
   - O que você já tentou
