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
      mutations: {
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

// Mock de dados para testes
export const mockDashboardGeralData = {
  financial_summary: {
    receita: 100000,
    despesa: 60000,
    lucro: 40000,
    variacao_receita: 15,
    variacao_despesa: 10,
    variacao_lucro: 20,
  },
  evolution_chart: {
    months: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    receita: [80000, 85000, 90000, 95000, 98000, 100000],
    despesa: [50000, 52000, 54000, 56000, 58000, 60000],
    lucro: [30000, 33000, 36000, 39000, 40000, 40000],
  },
};

export const mockDashboardFinancasData = {
  financial_summary: {
    receita: 100000,
    despesa: 60000,
    lucro: 40000,
    variacao_receita: 15,
    variacao_despesa: 10,
    variacao_lucro: 20,
  },
  evolution_chart: {
    months: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    receita: [80000, 85000, 90000, 95000, 98000, 100000],
    despesa: [50000, 52000, 54000, 56000, 58000, 60000],
    lucro: [30000, 33000, 36000, 39000, 40000, 40000],
  },
  top_expenses: {
    'Salários': { valor: 30000 },
    'Aluguel': { valor: 10000 },
    'Marketing': { valor: 8000 },
  },
  top_revenues: {
    'Vendas Online': { valor: 60000 },
    'Vendas Físicas': { valor: 40000 },
  },
};

export const mockAlertsData = {
  alerts: [
    {
      id: '1',
      type: 'warning' as const,
      category: 'Estoque',
      message: 'Produto X com estoque baixo',
      timestamp: new Date().toISOString(),
    },
    {
      id: '2',
      type: 'danger' as const,
      category: 'Financeiro',
      message: 'Despesas acima do orçamento',
      timestamp: new Date().toISOString(),
    },
  ],
  count: 2,
};

export * from '@testing-library/react';
