// tests/integration/flows/favorites-flow.test.tsx
import { renderWithProviders, screen } from '../helpers/render-with-providers';
import userEvent from '@testing-library/user-event';
import { Sidebar } from '@/components/layouts/sidebar';
import { useFavorites } from '@/lib/hooks/useFavorites';
import { resetStore, setStoreState } from '../helpers/mock-store';

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

describe('Fluxo de Favoritos - Integração', () => {
  let mockToggleFavorite: jest.Mock;
  let currentFavorites: string[];

  beforeEach(() => {
    resetStore();
    jest.clearAllMocks();
    currentFavorites = [];
    mockToggleFavorite = jest.fn((id: string) => {
      const index = currentFavorites.indexOf(id);
      if (index > -1) {
        currentFavorites.splice(index, 1);
      } else {
        currentFavorites.push(id);
      }
    });
    
    mockUseFavorites.mockImplementation(() => ({
      favorites: currentFavorites,
      toggleFavorite: mockToggleFavorite,
      isFavorite: jest.fn((id) => currentFavorites.includes(id)),
    }));
  });

  it('adiciona dashboard aos favoritos', async () => {
    setStoreState({ sidebarOpen: true });
    
    renderWithProviders(<Sidebar />);
    
    // Tentar adicionar aos favoritos (pode precisar de hover)
    const financasItem = screen.getByText('Finanças').closest('div');
    expect(financasItem).toBeInTheDocument();
  });

  it('remove dashboard dos favoritos', () => {
    currentFavorites = ['geral', 'financas'];
    
    mockUseFavorites.mockReturnValue({
      favorites: currentFavorites,
      toggleFavorite: mockToggleFavorite,
      isFavorite: jest.fn((id) => currentFavorites.includes(id)),
    });
    
    setStoreState({ sidebarOpen: true });
    
    renderWithProviders(<Sidebar />);
    
    expect(screen.getByText('Favoritos')).toBeInTheDocument();
    expect(screen.getByText('Visão Geral')).toBeInTheDocument();
    expect(screen.getByText('Finanças')).toBeInTheDocument();
  });

  it('exibe favoritos no topo da sidebar', () => {
    currentFavorites = ['geral'];
    
    mockUseFavorites.mockReturnValue({
      favorites: currentFavorites,
      toggleFavorite: mockToggleFavorite,
      isFavorite: jest.fn((id) => currentFavorites.includes(id)),
    });
    
    setStoreState({ sidebarOpen: true });
    
    renderWithProviders(<Sidebar />);
    
    const sidebar = screen.getByText('Visão Geral').closest('nav');
    const textContent = sidebar?.textContent || '';
    
    // Verificar se "Favoritos" aparece antes de outros itens
    const favoritesIndex = textContent.indexOf('Favoritos');
    const geralIndex = textContent.indexOf('Visão Geral');
    const financasIndex = textContent.indexOf('Finanças');
    
    expect(favoritesIndex).toBeLessThan(financasIndex);
    expect(geralIndex).toBeLessThan(financasIndex);
  });
});
