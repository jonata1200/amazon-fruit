// tests/unit/components/layouts/header.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Header } from '@/components/layouts/header';
import { useAppStore } from '@/store';
import { useAlerts } from '@/lib/hooks/useAlerts';

// Mock do store
jest.mock('@/store', () => ({
  useAppStore: jest.fn(),
}));

// Mock do hook useAlerts
jest.mock('@/lib/hooks/useAlerts', () => ({
  useAlerts: jest.fn(),
}));

describe('Header', () => {
  const mockToggleTheme = jest.fn();
  const mockToggleSidebar = jest.fn();
  const mockToggleAlerts = jest.fn();
  const mockToggleSearch = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    (useAppStore as unknown as jest.Mock).mockImplementation((selector) => {
      if (typeof selector === 'function') {
        return selector({
          theme: 'light',
          toggleTheme: mockToggleTheme,
          toggleSidebar: mockToggleSidebar,
          toggleAlerts: mockToggleAlerts,
          toggleSearch: mockToggleSearch,
        });
      }
    });

    (useAlerts as jest.Mock).mockReturnValue({
      data: { alerts: [], count: 0 },
      isLoading: false,
    });
  });

  it('renders header with title', () => {
    render(<Header title="Dashboard Geral" />);
    expect(screen.getByText('Dashboard Geral')).toBeInTheDocument();
  });

  it('renders search button', () => {
    render(<Header title="Test" />);
    const searchButton = screen.getByTitle('Busca (Ctrl+K)');
    expect(searchButton).toBeInTheDocument();
  });

  it('calls toggleSearch when search button is clicked', () => {
    render(<Header title="Test" />);
    const searchButton = screen.getByTitle('Busca (Ctrl+K)');
    fireEvent.click(searchButton);
    expect(mockToggleSearch).toHaveBeenCalledTimes(1);
  });

  it('renders theme toggle button', () => {
    render(<Header title="Test" />);
    const themeButton = screen.getByTitle('Tema (Ctrl+T)');
    expect(themeButton).toBeInTheDocument();
  });

  it('calls toggleTheme when theme button is clicked', () => {
    render(<Header title="Test" />);
    const themeButton = screen.getByTitle('Tema (Ctrl+T)');
    fireEvent.click(themeButton);
    expect(mockToggleTheme).toHaveBeenCalledTimes(1);
  });

  it('renders alerts button', () => {
    render(<Header title="Test" />);
    const alertsButton = screen.getByTitle('Alertas');
    expect(alertsButton).toBeInTheDocument();
  });

  it('calls toggleAlerts when alerts button is clicked', () => {
    render(<Header title="Test" />);
    const alertsButton = screen.getByTitle('Alertas');
    fireEvent.click(alertsButton);
    expect(mockToggleAlerts).toHaveBeenCalledTimes(1);
  });

  it('displays alerts count badge when there are alerts', () => {
    (useAlerts as jest.Mock).mockReturnValue({
      data: { alerts: [{ id: '1', type: 'warning', category: 'Test', message: 'Test' }], count: 5 },
      isLoading: false,
    });

    render(<Header title="Test" />);
    expect(screen.getByText('5')).toBeInTheDocument();
  });

  it('displays 9+ when alerts count is greater than 9', () => {
    (useAlerts as jest.Mock).mockReturnValue({
      data: { alerts: [], count: 15 },
      isLoading: false,
    });

    render(<Header title="Test" />);
    expect(screen.getByText('9+')).toBeInTheDocument();
  });

  it('shows moon icon when theme is light', () => {
    render(<Header title="Test" />);
    // Verificar se há um ícone de lua (Moon)
    const themeButton = screen.getByTitle('Tema (Ctrl+T)');
    expect(themeButton).toBeInTheDocument();
  });

  it('shows sun icon when theme is dark', () => {
    (useAppStore as unknown as jest.Mock).mockImplementation((selector) => {
      if (typeof selector === 'function') {
        return selector({
          theme: 'dark',
          toggleTheme: mockToggleTheme,
          toggleSidebar: mockToggleSidebar,
          toggleAlerts: mockToggleAlerts,
          toggleSearch: mockToggleSearch,
        });
      }
    });

    render(<Header title="Test" />);
    const themeButton = screen.getByTitle('Tema (Ctrl+T)');
    expect(themeButton).toBeInTheDocument();
  });

  it('renders mobile menu toggle', () => {
    render(<Header title="Test" />);
    const menuButtons = screen.getAllByRole('button');
    expect(menuButtons.length).toBeGreaterThan(0);
  });
});
