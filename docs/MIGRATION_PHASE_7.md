# 🧪 Fase 7: Integração e Testes

**Duração Estimada**: 5-7 dias  
**Complexidade**: Média  
**Dependências**: Fases 1-6 concluídas

---

## 🎯 Objetivos desta Fase

1. Implementar testes unitários abrangentes
2. Criar testes de integração
3. Implementar testes end-to-end (E2E)
4. Realizar testes de performance
5. Validar acessibilidade
6. Realizar testes de segurança
7. Validar compatibilidade cross-browser

---

## 📋 Checklist de Ações

### 1. Configuração de Testes Unitários

- [ ] **1.1** Verificar configuração do Jest (já feito na Fase 1)
- [ ] **1.2** Criar helpers de teste
  ```typescript
  // tests/helpers/test-utils.tsx
  import { render, RenderOptions } from '@testing-library/react';
  import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
  import { ReactElement } from 'react';

  const createTestQueryClient = () =>
    new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });

  export function renderWithProviders(
    ui: ReactElement,
    options?: Omit<RenderOptions, 'wrapper'>
  ) {
    const testQueryClient = createTestQueryClient();

    function Wrapper({ children }: { children: React.ReactNode }) {
      return (
        <QueryClientProvider client={testQueryClient}>
          {children}
        </QueryClientProvider>
      );
    }

    return render(ui, { wrapper: Wrapper, ...options });
  }

  export * from '@testing-library/react';
  ```

---

### 2. Testes Unitários - Componentes de UI

- [ ] **2.1** Testes do Button
  ```typescript
  // src/components/ui/__tests__/button.test.tsx
  import { render, screen, fireEvent } from '@testing-library/react';
  import { Button } from '../button';

  describe('Button', () => {
    it('renders correctly', () => {
      render(<Button>Click me</Button>);
      expect(screen.getByText('Click me')).toBeInTheDocument();
    });

    it('handles click events', () => {
      const handleClick = jest.fn();
      render(<Button onClick={handleClick}>Click me</Button>);
      
      fireEvent.click(screen.getByText('Click me'));
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('can be disabled', () => {
      render(<Button disabled>Click me</Button>);
      expect(screen.getByText('Click me')).toBeDisabled();
    });

    it('applies variant styles', () => {
      const { rerender } = render(<Button variant="destructive">Delete</Button>);
      expect(screen.getByText('Delete')).toHaveClass('bg-destructive');

      rerender(<Button variant="outline">Cancel</Button>);
      expect(screen.getByText('Cancel')).toHaveClass('border');
    });
  });
  ```

- [ ] **2.2** Testes do Card
- [ ] **2.3** Testes do Input
- [ ] **2.4** Testes do KPICard

---

### 3. Testes Unitários - Hooks

- [ ] **3.1** Testes de hooks customizados
  ```typescript
  // src/lib/hooks/__tests__/useDashboards.test.ts
  import { renderHook, waitFor } from '@testing-library/react';
  import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
  import { useDashboardGeral } from '../useDashboards';

  const createWrapper = () => {
    const queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
      },
    });

    return ({ children }: { children: React.ReactNode }) => (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    );
  };

  describe('useDashboardGeral', () => {
    it('fetches dashboard data', async () => {
      const { result } = renderHook(
        () => useDashboardGeral({ start: '2024-01-01', end: '2024-12-31' }),
        { wrapper: createWrapper() }
      );

      await waitFor(() => expect(result.current.isSuccess).toBe(true));

      expect(result.current.data).toBeDefined();
    });
  });
  ```

- [ ] **3.2** Testes do useAlerts
- [ ] **3.3** Testes do useDebounce
- [ ] **3.4** Testes do useKeyboardShortcuts

---

### 4. Testes Unitários - Utilitários

- [ ] **4.1** Testes de formatadores
  ```typescript
  // src/lib/utils/__tests__/formatters.test.ts
  import { 
    formatCurrency, 
    formatNumber, 
    formatPercentage,
    formatDate
  } from '../formatters';

  describe('Formatters', () => {
    describe('formatCurrency', () => {
      it('formats positive values', () => {
        expect(formatCurrency(1000)).toBe('R$ 1.000,00');
        expect(formatCurrency(1234.56)).toBe('R$ 1.234,56');
      });

      it('formats negative values', () => {
        expect(formatCurrency(-500)).toBe('-R$ 500,00');
      });

      it('formats zero', () => {
        expect(formatCurrency(0)).toBe('R$ 0,00');
      });
    });

    describe('formatNumber', () => {
      it('formats with specified decimals', () => {
        expect(formatNumber(1000.5, 2)).toBe('1.000,50');
        expect(formatNumber(1234.567, 1)).toBe('1.234,6');
      });

      it('formats without decimals', () => {
        expect(formatNumber(1000)).toBe('1.000');
      });
    });

    describe('formatPercentage', () => {
      it('formats percentage values', () => {
        expect(formatPercentage(15.5)).toBe('15,5%');
        expect(formatPercentage(100)).toBe('100,0%');
      });
    });

    describe('formatDate', () => {
      it('formats date strings', () => {
        const date = '2024-01-15';
        expect(formatDate(date)).toBe('15/01/2024');
      });
    });
  });
  ```

- [ ] **4.2** Testes de validadores
  ```typescript
  // src/lib/utils/__tests__/validators.test.ts
  import { isValidDate, isValidDateRange, isValidEmail } from '../validators';

  describe('Validators', () => {
    describe('isValidDate', () => {
      it('validates correct date format', () => {
        expect(isValidDate('2024-01-15')).toBe(true);
        expect(isValidDate('2024-12-31')).toBe(true);
      });

      it('rejects invalid formats', () => {
        expect(isValidDate('15-01-2024')).toBe(false);
        expect(isValidDate('2024/01/15')).toBe(false);
        expect(isValidDate('invalid')).toBe(false);
      });
    });

    describe('isValidDateRange', () => {
      it('validates correct date ranges', () => {
        expect(isValidDateRange('2024-01-01', '2024-12-31')).toBe(true);
      });

      it('rejects invalid ranges', () => {
        expect(isValidDateRange('2024-12-31', '2024-01-01')).toBe(false);
      });
    });

    describe('isValidEmail', () => {
      it('validates correct emails', () => {
        expect(isValidEmail('test@example.com')).toBe(true);
        expect(isValidEmail('user.name@domain.co.uk')).toBe(true);
      });

      it('rejects invalid emails', () => {
        expect(isValidEmail('invalid')).toBe(false);
        expect(isValidEmail('@example.com')).toBe(false);
      });
    });
  });
  ```

---

### 5. Testes de Integração

- [ ] **5.1** Configurar MSW (Mock Service Worker) para mockar API
  ```bash
  npm install -D msw
  ```

  ```typescript
  // tests/mocks/handlers.ts
  import { rest } from 'msw';

  export const handlers = [
    rest.get('/api/dashboard/geral', (req, res, ctx) => {
      return res(
        ctx.status(200),
        ctx.json({
          status: 'success',
          period: { start: '2024-01-01', end: '2024-12-31' },
          financial_summary: {
            receita: 100000,
            despesa: 60000,
            lucro: 40000,
          },
          evolution_chart: {
            months: ['Jan', 'Feb', 'Mar'],
            receita: [10000, 15000, 20000],
            despesa: [6000, 8000, 10000],
            lucro: [4000, 7000, 10000],
          },
        })
      );
    }),

    rest.get('/api/alerts', (req, res, ctx) => {
      return res(
        ctx.status(200),
        ctx.json({
          status: 'success',
          alerts: [],
          count: 0,
        })
      );
    }),
  ];
  ```

  ```typescript
  // tests/mocks/server.ts
  import { setupServer } from 'msw/node';
  import { handlers } from './handlers';

  export const server = setupServer(...handlers);
  ```

- [ ] **5.2** Configurar MSW no Jest
  ```typescript
  // jest.setup.js
  import '@testing-library/jest-dom';
  import { server } from './tests/mocks/server';

  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());
  ```

- [ ] **5.3** Testes de integração de Dashboard
  ```typescript
  // tests/integration/dashboard-geral.test.tsx
  import { screen, waitFor } from '@testing-library/react';
  import { renderWithProviders } from '../helpers/test-utils';
  import DashboardGeralPage from '@/app/(dashboards)/geral/page';

  describe('Dashboard Geral Integration', () => {
    it('loads and displays dashboard data', async () => {
      renderWithProviders(<DashboardGeralPage />);

      // Verifica loading
      expect(screen.getByText(/carregando/i)).toBeInTheDocument();

      // Aguarda dados carregarem
      await waitFor(() => {
        expect(screen.getByText('Receita Total')).toBeInTheDocument();
      });

      // Verifica KPIs
      expect(screen.getByText('R$ 100.000,00')).toBeInTheDocument();
    });

    it('handles API errors gracefully', async () => {
      // Mock de erro
      server.use(
        rest.get('/api/dashboard/geral', (req, res, ctx) => {
          return res(ctx.status(500));
        })
      );

      renderWithProviders(<DashboardGeralPage />);

      await waitFor(() => {
        expect(screen.getByText(/erro/i)).toBeInTheDocument();
      });
    });
  });
  ```

- [ ] **5.4** Testes de fluxo de navegação
- [ ] **5.5** Testes de integração de alertas
- [ ] **5.6** Testes de integração de busca

---

### 6. Testes End-to-End (E2E)

- [ ] **6.1** Instalar Playwright
  ```bash
  npm install -D @playwright/test
  npx playwright install
  ```

- [ ] **6.2** Configurar Playwright
  ```typescript
  // playwright.config.ts
  import { defineConfig, devices } from '@playwright/test';

  export default defineConfig({
    testDir: './tests/e2e',
    fullyParallel: true,
    forbidOnly: !!process.env.CI,
    retries: process.env.CI ? 2 : 0,
    workers: process.env.CI ? 1 : undefined,
    reporter: 'html',
    use: {
      baseURL: 'http://localhost:3000',
      trace: 'on-first-retry',
    },

    projects: [
      {
        name: 'chromium',
        use: { ...devices['Desktop Chrome'] },
      },
      {
        name: 'firefox',
        use: { ...devices['Desktop Firefox'] },
      },
      {
        name: 'webkit',
        use: { ...devices['Desktop Safari'] },
      },
      {
        name: 'Mobile Chrome',
        use: { ...devices['Pixel 5'] },
      },
    ],

    webServer: {
      command: 'npm run dev',
      url: 'http://localhost:3000',
      reuseExistingServer: !process.env.CI,
    },
  });
  ```

- [ ] **6.3** Criar testes E2E de navegação
  ```typescript
  // tests/e2e/navigation.spec.ts
  import { test, expect } from '@playwright/test';

  test.describe('Navigation', () => {
    test('should navigate between dashboards', async ({ page }) => {
      await page.goto('/');

      // Deve redirecionar para /geral
      await expect(page).toHaveURL('/geral');

      // Clica no menu de Finanças
      await page.click('text=Finanças');
      await expect(page).toHaveURL('/financas');
      await expect(page.getByRole('heading', { name: 'Dashboard de Finanças' })).toBeVisible();

      // Clica no menu de Estoque
      await page.click('text=Estoque');
      await expect(page).toHaveURL('/estoque');
      await expect(page.getByRole('heading', { name: 'Dashboard de Estoque' })).toBeVisible();
    });
  });
  ```

- [ ] **6.4** Testes E2E de funcionalidades
  ```typescript
  // tests/e2e/features.spec.ts
  import { test, expect } from '@playwright/test';

  test.describe('Features', () => {
    test('should open and close alerts panel', async ({ page }) => {
      await page.goto('/geral');

      // Clica no botão de alertas
      await page.click('[title="Alertas"]');
      
      // Verifica se painel abriu
      await expect(page.getByText('Alertas do Sistema')).toBeVisible();

      // Fecha o painel
      await page.click('button:has-text("✕")');
      await expect(page.getByText('Alertas do Sistema')).not.toBeVisible();
    });

    test('should open search with keyboard shortcut', async ({ page }) => {
      await page.goto('/geral');

      // Pressiona Ctrl+F
      await page.keyboard.press('Control+f');

      // Verifica se busca abriu
      await expect(page.getByPlaceholder(/buscar/i)).toBeVisible();
    });

    test('should toggle theme', async ({ page }) => {
      await page.goto('/geral');

      // Verifica tema inicial
      const html = page.locator('html');
      await expect(html).toHaveClass(/light/);

      // Clica no botão de tema
      await page.click('[title*="Tema"]');

      // Verifica se mudou para dark
      await expect(html).toHaveClass(/dark/);
    });
  });
  ```

- [ ] **6.5** Testes E2E de formulários
- [ ] **6.6** Testes E2E de exportação

---

### 7. Testes de Performance

- [ ] **7.1** Configurar Lighthouse CI
  ```bash
  npm install -D @lhci/cli
  ```

  ```json
  // lighthouserc.json
  {
    "ci": {
      "collect": {
        "startServerCommand": "npm run build && npm run start",
        "url": [
          "http://localhost:3000/geral",
          "http://localhost:3000/financas",
          "http://localhost:3000/estoque"
        ],
        "numberOfRuns": 3
      },
      "assert": {
        "preset": "lighthouse:recommended",
        "assertions": {
          "categories:performance": ["error", { "minScore": 0.9 }],
          "categories:accessibility": ["error", { "minScore": 0.9 }],
          "categories:best-practices": ["error", { "minScore": 0.9 }],
          "categories:seo": ["error", { "minScore": 0.9 }]
        }
      }
    }
  }
  ```

- [ ] **7.2** Adicionar script de performance
  ```json
  // package.json
  {
    "scripts": {
      "lighthouse": "lhci autorun"
    }
  }
  ```

- [ ] **7.3** Executar testes de performance
  ```bash
  npm run lighthouse
  ```

- [ ] **7.4** Analisar e otimizar baseado nos resultados

---

### 8. Testes de Acessibilidade

- [ ] **8.1** Instalar ferramentas de acessibilidade
  ```bash
  npm install -D @axe-core/react jest-axe
  ```

- [ ] **8.2** Criar testes de acessibilidade
  ```typescript
  // tests/a11y/accessibility.test.tsx
  import { render } from '@testing-library/react';
  import { axe, toHaveNoViolations } from 'jest-axe';
  import DashboardGeralPage from '@/app/(dashboards)/geral/page';

  expect.extend(toHaveNoViolations);

  describe('Accessibility', () => {
    it('should not have any accessibility violations', async () => {
      const { container } = render(<DashboardGeralPage />);
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });
  ```

- [ ] **8.3** Validar navegação por teclado
- [ ] **8.4** Validar ARIA labels
- [ ] **8.5** Testar com leitor de tela

---

### 9. Testes de Segurança

- [ ] **9.1** Verificar vulnerabilidades de dependências
  ```bash
  npm audit
  npm audit fix
  ```

- [ ] **9.2** Implementar Content Security Policy
  ```typescript
  // next.config.js
  const securityHeaders = [
    {
      key: 'X-DNS-Prefetch-Control',
      value: 'on'
    },
    {
      key: 'X-Frame-Options',
      value: 'SAMEORIGIN'
    },
    {
      key: 'X-Content-Type-Options',
      value: 'nosniff'
    },
  ];

  module.exports = {
    async headers() {
      return [
        {
          source: '/:path*',
          headers: securityHeaders,
        },
      ];
    },
  };
  ```

- [ ] **9.3** Validar inputs do usuário
- [ ] **9.4** Testar proteção contra XSS
- [ ] **9.5** Validar autenticação (se aplicável)

---

### 10. Cobertura de Testes

- [ ] **10.1** Configurar cobertura de testes
  ```json
  // package.json
  {
    "scripts": {
      "test:coverage": "jest --coverage"
    },
    "jest": {
      "collectCoverageFrom": [
        "src/**/*.{js,jsx,ts,tsx}",
        "!src/**/*.d.ts",
        "!src/**/*.stories.{js,jsx,ts,tsx}",
        "!src/**/__tests__/**"
      ],
      "coverageThresholds": {
        "global": {
          "branches": 80,
          "functions": 80,
          "lines": 80,
          "statements": 80
        }
      }
    }
  }
  ```

- [ ] **10.2** Executar relatório de cobertura
  ```bash
  npm run test:coverage
  ```

- [ ] **10.3** Analisar e melhorar cobertura

---

### 11. CI/CD Pipeline

- [ ] **11.1** Criar workflow do GitHub Actions
  ```yaml
  # .github/workflows/ci.yml
  name: CI

  on:
    push:
      branches: [main, develop]
    pull_request:
      branches: [main, develop]

  jobs:
    test:
      runs-on: ubuntu-latest

      steps:
        - uses: actions/checkout@v3
        
        - name: Setup Node.js
          uses: actions/setup-node@v3
          with:
            node-version: '18'
            cache: 'npm'
        
        - name: Install dependencies
          run: npm ci
        
        - name: Run linting
          run: npm run lint
        
        - name: Run type check
          run: npm run type-check
        
        - name: Run tests
          run: npm run test:coverage
        
        - name: Build
          run: npm run build
        
        - name: Run E2E tests
          run: npx playwright test
  ```

---

### 12. Documentação de Testes

- [ ] **12.1** Documentar estratégia de testes
- [ ] **12.2** Criar guia de como escrever testes
- [ ] **12.3** Documentar casos de teste importantes
- [ ] **12.4** Criar guia de troubleshooting de testes

---

### 13. Verificação Final

- [ ] **13.1** Executar todos os testes
  ```bash
  npm test
  npm run test:coverage
  npx playwright test
  npm run lighthouse
  ```

- [ ] **13.2** Verificar cobertura de testes > 80%
- [ ] **13.3** Validar performance scores > 90
- [ ] **13.4** Validar acessibilidade scores > 90
- [ ] **13.5** Commit das mudanças
  ```bash
  git add .
  git commit -m "test: implementar testes completos"
  ```

---

## ✅ Critérios de Conclusão da Fase 7

A Fase 7 está completa quando:

- [x] Cobertura de testes > 80%
- [x] Testes unitários passando
- [x] Testes de integração passando
- [x] Testes E2E passando
- [x] Performance score > 90
- [x] Acessibilidade score > 90
- [x] Zero vulnerabilidades de segurança críticas
- [x] CI/CD configurado
- [x] Documentação de testes completa

---

## 📝 Notas e Observações

### Próximos Passos

- Prosseguir para [Fase 8: Deploy e Otimização](./MIGRATION_PHASE_8.md)

---

**Status**: ⏳ Pendente  
**Responsável**: [Nome]  
**Data de Início**: [Data]  
**Data de Conclusão**: [Data]
