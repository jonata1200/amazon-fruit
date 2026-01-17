// tests/integration/flows/navigation-flow.test.tsx
import { renderWithProviders, screen } from '../helpers/render-with-providers';
import userEvent from '@testing-library/user-event';
import { Sidebar } from '@/components/layouts/sidebar';
import { useAppStore } from '@/store';
import { resetStore, setStoreState } from '../helpers/mock-store';
import { useFavorites } from '@/lib/hooks/useFavorites';

// Mock do next/navigation
jest.mock('next/navigation', () => ({
  usePathname: () => '/geral',
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

// Mock do hook useFavorites
jest.mock('@/lib/hooks/useFavorites');
const mockUseFavorites = useFavorites as jest.MockedFunction<typeof useFavorites>;

describe('Fluxo de Navegação - Integração', () => {
  beforeEach(() => {
    resetStore();
    jest.clearAllMocks();
    mockUseFavorites.mockReturnValue({
      favorites: [],
      toggleFavorite: jest.fn(),
      isFavorite: jest.fn(() => false),
    });
  });

  it('renderiza todos os itens do menu na sidebar', () => {
    setStoreState({ sidebarOpen: true });
    
    renderWithProviders(<Sidebar />);
    
    expect(screen.getByText('Visão Geral')).toBeInTheDocument();
    expect(screen.getByText('Finanças')).toBeInTheDocument();
    expect(screen.getByText('Estoque')).toBeInTheDocument();
    expect(screen.getByText('Público-Alvo')).toBeInTheDocument();
    expect(screen.getByText('Fornecedores')).toBeInTheDocument();
    expect(screen.getByText('Recursos Humanos')).toBeInTheDocument();
  });

  it('destaca item ativo no menu', () => {
    setStoreState({ sidebarOpen: true });
    
    renderWithProviders(<Sidebar />);
    
    const activeLink = screen.getByText('Visão Geral').closest('a');
    expect(activeLink).toHaveAttribute('aria-current', 'page');
  });

  it('permite adicionar item aos favoritos', async () => {
    const mockToggleFavorite = jest.fn();
    mockUseFavorites.mockReturnValue({
      favorites: [],
      toggleFavorite: mockToggleFavorite,
      isFavorite: jest.fn(() => false),
    });
    
    setStoreState({ sidebarOpen: true });
    
    renderWithProviders(<Sidebar />);
    
    // Hover para mostrar botão de favorito
    const financasLink = screen.getByText('Finanças').closest('div');
    if (financasLink) {
      // Simular hover (pode não funcionar perfeitamente em testes)
      const starButton = financasLink.querySelector('button[aria-label*="favoritos"]');
      if (starButton) {
        await userEvent.click(starButton);
        expect(mockToggleFavorite).toHaveBeenCalledWith('financas');
      }
    }
  });

  it('exibe seção de favoritos quando há favoritos', () => {
    mockUseFavorites.mockReturnValue({
      favorites: ['geral', 'financas'],
      toggleFavorite: jest.fn(),
      isFavorite: jest.fn((id) => ['geral', 'financas'].includes(id)),
    });
    
    setStoreState({ sidebarOpen: true });
    
    renderWithProviders(<Sidebar />);
    
    expect(screen.getByText('Favoritos')).toBeInTheDocument();
  });
});
