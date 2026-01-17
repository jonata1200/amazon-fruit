// tests/integration/features/alerts-system.test.tsx
import { renderWithProviders, screen, waitFor } from '../helpers/render-with-providers';
import { AlertsPanel } from '@/components/features/alerts/alerts-panel';
import { useAlerts } from '@/lib/hooks/useAlerts';
import { resetStore, setStoreState } from '../helpers/mock-store';

// Mock do hook useAlerts
jest.mock('@/lib/hooks/useAlerts');
const mockUseAlerts = useAlerts as jest.MockedFunction<typeof useAlerts>;

const mockAlertsResponse = {
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

describe('Sistema de Alertas - Integração', () => {
  beforeEach(() => {
    resetStore();
    jest.clearAllMocks();
  });

  it('renderiza painel de alertas quando aberto', () => {
    setStoreState({ alertsOpen: true });
    mockUseAlerts.mockReturnValue({
      data: mockAlertsResponse,
      isLoading: false,
      isError: false,
      error: null,
      isSuccess: true,
      refetch: jest.fn(),
    });

    renderWithProviders(<AlertsPanel />);
    
    expect(screen.getByText('Alertas do Sistema')).toBeInTheDocument();
  });

  it('não renderiza quando alertsOpen é false', () => {
    setStoreState({ alertsOpen: false });
    
    const { container } = renderWithProviders(<AlertsPanel />);
    
    expect(container.firstChild).toBeNull();
  });

  it('exibe alertas quando há dados', () => {
    setStoreState({ alertsOpen: true });
    mockUseAlerts.mockReturnValue({
      data: mockAlertsResponse,
      isLoading: false,
      isError: false,
      error: null,
      isSuccess: true,
      refetch: jest.fn(),
    });

    renderWithProviders(<AlertsPanel />);
    
    expect(screen.getByText('Produto X com estoque baixo')).toBeInTheDocument();
    expect(screen.getByText('Despesas acima do orçamento')).toBeInTheDocument();
    expect(screen.getByText('Estoque')).toBeInTheDocument();
    expect(screen.getByText('Financeiro')).toBeInTheDocument();
  });

  it('exibe skeleton durante carregamento', () => {
    setStoreState({ alertsOpen: true });
    mockUseAlerts.mockReturnValue({
      data: undefined,
      isLoading: true,
      isError: false,
      error: null,
      isSuccess: false,
      refetch: jest.fn(),
    });

    renderWithProviders(<AlertsPanel />);
    
    // Verificar se há elementos de skeleton
    const skeletons = document.querySelectorAll('[class*="Skeleton"]');
    expect(skeletons.length).toBeGreaterThan(0);
  });

  it('exibe mensagem quando não há alertas', () => {
    setStoreState({ alertsOpen: true });
    mockUseAlerts.mockReturnValue({
      data: { alerts: [], count: 0 },
      isLoading: false,
      isError: false,
      error: null,
      isSuccess: true,
      refetch: jest.fn(),
    });

    renderWithProviders(<AlertsPanel />);
    
    expect(screen.getByText('Nenhum alerta no momento')).toBeInTheDocument();
  });

  it('exibe contador de alertas no footer', () => {
    setStoreState({ alertsOpen: true });
    mockUseAlerts.mockReturnValue({
      data: mockAlertsResponse,
      isLoading: false,
      isError: false,
      error: null,
      isSuccess: true,
      refetch: jest.fn(),
    });

    renderWithProviders(<AlertsPanel />);
    
    expect(screen.getByText(/Total: 2 alertas/i)).toBeInTheDocument();
  });

  it('fecha painel ao clicar no botão de fechar', async () => {
    setStoreState({ alertsOpen: true });
    mockUseAlerts.mockReturnValue({
      data: mockAlertsResponse,
      isLoading: false,
      isError: false,
      error: null,
      isSuccess: true,
      refetch: jest.fn(),
    });

    renderWithProviders(<AlertsPanel />);
    
    const closeButton = screen.getByLabelText('Fechar painel de alertas');
    closeButton.click();
    
    await waitFor(() => {
      const { useAppStore } = require('@/store');
      expect(useAppStore.getState().alertsOpen).toBe(false);
    });
  });

  it('exibe diferentes tipos de alertas com cores corretas', () => {
    setStoreState({ alertsOpen: true });
    mockUseAlerts.mockReturnValue({
      data: mockAlertsResponse,
      isLoading: false,
      isError: false,
      error: null,
      isSuccess: true,
      refetch: jest.fn(),
    });

    renderWithProviders(<AlertsPanel />);
    
    // Verificar se os alertas são renderizados com classes de cor
    const warningAlert = screen.getByText('Estoque').closest('[class*="border-l-yellow"]');
    const dangerAlert = screen.getByText('Financeiro').closest('[class*="border-l-red"]');
    
    expect(warningAlert).toBeInTheDocument();
    expect(dangerAlert).toBeInTheDocument();
  });
});
