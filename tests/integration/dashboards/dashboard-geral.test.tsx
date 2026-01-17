// tests/integration/dashboards/dashboard-geral.test.tsx
import { renderWithProviders, screen, waitFor } from '../helpers/render-with-providers';
import userEvent from '@testing-library/user-event';
import { PeriodSelector } from '@/components/dashboards/period-selector';
import { KPICard } from '@/components/dashboards/kpi-card';
import { useAppStore } from '@/store';
import { resetStore } from '../helpers/mock-store';

describe('Dashboard Geral - Integração', () => {
  beforeEach(() => {
    resetStore();
    jest.clearAllMocks();
  });

  it('renderiza seletor de período', () => {
    renderWithProviders(<PeriodSelector />);
    
    expect(screen.getByText(/Período/i)).toBeInTheDocument();
  });

  it('atualiza período no store ao aplicar', async () => {
    renderWithProviders(<PeriodSelector />);
    
    const startInput = screen.getByLabelText('Data Inicial');
    const endInput = screen.getByLabelText('Data Final');
    const applyButton = screen.getByText('Aplicar Período');
    
    await userEvent.type(startInput, '2024-01-01');
    await userEvent.type(endInput, '2024-12-31');
    await userEvent.click(applyButton);
    
    await waitFor(() => {
      const store = useAppStore.getState();
      expect(store.dateRange.start).toBe('2024-01-01');
      expect(store.dateRange.end).toBe('2024-12-31');
    });
  });

  it('renderiza KPIs com dados', () => {
    const kpiData = {
      title: 'Receita',
      value: 100000,
      change: 15,
      changeType: 'increase' as const,
      format: 'currency' as const,
    };

    renderWithProviders(<KPICard {...kpiData} />);
    
    expect(screen.getByText('Receita')).toBeInTheDocument();
    // Verificar se o valor está presente (formatado como moeda)
    expect(screen.getByText(/R\$/i)).toBeInTheDocument();
  });

  it('exibe variação positiva corretamente', () => {
    const kpiData = {
      title: 'Lucro',
      value: 40000,
      change: 20,
      changeType: 'increase' as const,
      format: 'currency' as const,
    };

    renderWithProviders(<KPICard {...kpiData} />);
    
    // Verificar se há texto "vs período anterior" e porcentagem
    expect(screen.getByText(/vs período anterior/i)).toBeInTheDocument();
    expect(screen.getByText(/20%/i)).toBeInTheDocument();
  });

  it('exibe variação negativa corretamente', () => {
    const kpiData = {
      title: 'Despesa',
      value: 60000,
      change: 10,
      changeType: 'decrease' as const,
      format: 'currency' as const,
    };

    renderWithProviders(<KPICard {...kpiData} />);
    
    // Verificar se há texto "vs período anterior" e porcentagem
    expect(screen.getByText(/vs período anterior/i)).toBeInTheDocument();
    expect(screen.getByText(/10%/i)).toBeInTheDocument();
  });
});
