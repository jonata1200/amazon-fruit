// tests/integration/features/global-search.test.tsx
import { renderWithProviders, screen, waitFor, fireEvent } from '../helpers/render-with-providers';
import userEvent from '@testing-library/user-event';
import { GlobalSearch } from '@/components/features/search/global-search';
import { useAppStore } from '@/store';
import { resetStore, setStoreState } from '../helpers/mock-store';

const mockPush = jest.fn();

// Mock do next/navigation
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

describe('GlobalSearch - Integração', () => {
  beforeEach(() => {
    resetStore();
    jest.clearAllMocks();
  });

  it('abre e fecha a busca global', async () => {
    setStoreState({ searchOpen: true });
    
    renderWithProviders(<GlobalSearch />);
    
    expect(screen.getByPlaceholderText('Buscar em todos os dashboards...')).toBeInTheDocument();
    
    // O botão de fechar é um ícone X dentro de um botão
    const closeButton = screen.getByRole('button').querySelector('svg')?.closest('button');
    if (closeButton) {
      await userEvent.click(closeButton);
      
      await waitFor(() => {
        expect(useAppStore.getState().searchOpen).toBe(false);
      });
    }
  });

  it('não renderiza quando searchOpen é false', () => {
    setStoreState({ searchOpen: false });
    
    const { container } = renderWithProviders(<GlobalSearch />);
    
    expect(container.firstChild).toBeNull();
  });

  it('realiza busca e exibe resultados', async () => {
    setStoreState({ searchOpen: true });
    
    renderWithProviders(<GlobalSearch />);
    
    const input = screen.getByPlaceholderText('Buscar em todos os dashboards...');
    
    await userEvent.type(input, 'geral');
    
    await waitFor(() => {
      expect(screen.getByText('Dashboard Geral')).toBeInTheDocument();
    }, { timeout: 2000 });
  });

  it('exibe mensagem quando query é muito curta', async () => {
    setStoreState({ searchOpen: true });
    
    renderWithProviders(<GlobalSearch />);
    
    const input = screen.getByPlaceholderText('Buscar em todos os dashboards...');
    
    await userEvent.type(input, 'ge');
    
    await waitFor(() => {
      expect(screen.getByText(/Digite pelo menos 3 caracteres/i)).toBeInTheDocument();
    });
  });

  it('navega para resultado ao clicar', async () => {
    setStoreState({ searchOpen: true });
    
    renderWithProviders(<GlobalSearch />);
    
    const input = screen.getByPlaceholderText('Buscar em todos os dashboards...');
    await userEvent.type(input, 'geral');
    
    await waitFor(() => {
      expect(screen.getByText('Dashboard Geral')).toBeInTheDocument();
    }, { timeout: 2000 });
    
    const resultButton = screen.getByText('Dashboard Geral').closest('button');
    if (resultButton) {
      await userEvent.click(resultButton);
      
      await waitFor(() => {
        expect(useAppStore.getState().searchOpen).toBe(false);
      });
      expect(mockPush).toHaveBeenCalledWith('/geral');
    }
  });

  it('fecha ao clicar no overlay', async () => {
    setStoreState({ searchOpen: true });
    
    const { container } = renderWithProviders(<GlobalSearch />);
    
    const overlay = container.querySelector('.fixed.inset-0');
    if (overlay) {
      fireEvent.click(overlay);
      
      await waitFor(() => {
        expect(useAppStore.getState().searchOpen).toBe(false);
      });
    }
  });
});
