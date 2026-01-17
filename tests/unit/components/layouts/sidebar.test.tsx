// tests/unit/components/layouts/sidebar.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Sidebar } from '@/components/layouts/sidebar';
import { useAppStore } from '@/store';
import { useFavorites } from '@/lib/hooks/useFavorites';

// Mock do next/navigation
jest.mock('next/navigation', () => ({
  usePathname: () => '/geral',
}));

// Mock do store
jest.mock('@/store', () => ({
  useAppStore: jest.fn(),
}));

// Mock do hook useFavorites
jest.mock('@/lib/hooks/useFavorites', () => ({
  useFavorites: jest.fn(),
}));

describe('Sidebar', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (useAppStore as unknown as jest.Mock).mockImplementation((selector) => {
      if (typeof selector === 'function') {
        return selector({
          sidebarOpen: true,
        });
      }
    });

    (useFavorites as jest.Mock).mockReturnValue({
      favorites: [],
      toggleFavorite: jest.fn(),
      isFavorite: jest.fn(() => false),
    });
  });

  it('renders sidebar', () => {
    render(<Sidebar />);
    expect(screen.getByText('Amazon Fruit')).toBeInTheDocument();
  });

  it('renders all menu items', () => {
    render(<Sidebar />);
    expect(screen.getByText('Visão Geral')).toBeInTheDocument();
    expect(screen.getByText('Finanças')).toBeInTheDocument();
    expect(screen.getByText('Estoque')).toBeInTheDocument();
    expect(screen.getByText('Público-Alvo')).toBeInTheDocument();
    expect(screen.getByText('Fornecedores')).toBeInTheDocument();
    expect(screen.getByText('Recursos Humanos')).toBeInTheDocument();
  });

  it('highlights active menu item', () => {
    render(<Sidebar />);
    const activeLink = screen.getByText('Visão Geral').closest('a');
    expect(activeLink).toHaveAttribute('aria-current', 'page');
  });

  it('renders favorites section when there are favorites', () => {
    (useFavorites as jest.Mock).mockReturnValue({
      favorites: ['geral', 'financas'],
      toggleFavorite: jest.fn(),
      isFavorite: jest.fn((id) => ['geral', 'financas'].includes(id)),
    });

    render(<Sidebar />);
    expect(screen.getByText('Favoritos')).toBeInTheDocument();
  });

  it('does not render favorites section when there are no favorites', () => {
    (useFavorites as jest.Mock).mockReturnValue({
      favorites: [],
      toggleFavorite: jest.fn(),
      isFavorite: jest.fn(() => false),
    });

    render(<Sidebar />);
    expect(screen.queryByText('Favoritos')).not.toBeInTheDocument();
  });

  it('calls toggleFavorite when star button is clicked', () => {
    const mockToggleFavorite = jest.fn();
    (useFavorites as jest.Mock).mockReturnValue({
      favorites: [],
      toggleFavorite: mockToggleFavorite,
      isFavorite: jest.fn(() => false),
    });

    render(<Sidebar />);
    const starButtons = screen.getAllByLabelText('Adicionar aos favoritos');
    if (starButtons.length > 0) {
      fireEvent.click(starButtons[0]);
      expect(mockToggleFavorite).toHaveBeenCalled();
    }
  });

  it('hides sidebar when sidebarOpen is false', () => {
    (useAppStore as unknown as jest.Mock).mockImplementation((selector) => {
      if (typeof selector === 'function') {
        return selector({
          sidebarOpen: false,
        });
      }
    });

    const { container } = render(<Sidebar />);
    const sidebar = container.querySelector('aside');
    expect(sidebar).toHaveClass('-translate-x-full');
  });
});
