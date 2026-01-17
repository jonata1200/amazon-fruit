// tests/integration/flows/theme-flow.test.tsx
import { renderWithProviders, screen } from '../helpers/render-with-providers';
import userEvent from '@testing-library/user-event';
import { Header } from '@/components/layouts/header';
import { useAppStore } from '@/store';
import { resetStore, setStoreState } from '../helpers/mock-store';
import { useAlerts } from '@/lib/hooks/useAlerts';

// Mock do hook useAlerts
jest.mock('@/lib/hooks/useAlerts');
const mockUseAlerts = useAlerts as jest.MockedFunction<typeof useAlerts>;

describe('Fluxo de Tema - Integração', () => {
  beforeEach(() => {
    resetStore();
    jest.clearAllMocks();
    mockUseAlerts.mockReturnValue({
      data: { alerts: [], count: 0 },
      isLoading: false,
      isError: false,
      error: null,
      isSuccess: true,
      refetch: jest.fn(),
    });
  });

  it('inicia com tema light', () => {
    setStoreState({ theme: 'light' });
    
    renderWithProviders(<Header title="Test" />);
    
    const themeButton = screen.getByTitle('Tema (Ctrl+T)');
    expect(themeButton).toBeInTheDocument();
  });

  it('alterna tema ao clicar no botão', async () => {
    setStoreState({ theme: 'light' });
    
    renderWithProviders(<Header title="Test" />);
    
    const themeButton = screen.getByTitle('Tema (Ctrl+T)');
    await userEvent.click(themeButton);
    
    expect(useAppStore.getState().theme).toBe('dark');
    
    await userEvent.click(themeButton);
    
    expect(useAppStore.getState().theme).toBe('light');
  });

  it('persiste tema no store', () => {
    setStoreState({ theme: 'dark' });
    
    renderWithProviders(<Header title="Test" />);
    
    expect(useAppStore.getState().theme).toBe('dark');
  });
});
