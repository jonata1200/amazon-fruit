// src/components/features/__tests__/global-search.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { GlobalSearch } from '../search/global-search';
import { useAppStore } from '@/store';

// Mock do router
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

// Mock do store
jest.mock('@/store', () => ({
  useAppStore: jest.fn(),
}));

describe('GlobalSearch', () => {
  beforeEach(() => {
    (useAppStore as unknown as jest.Mock).mockImplementation((selector) =>
      selector({
        searchOpen: true,
        setSearchOpen: jest.fn(),
      })
    );
  });

  it('renders search modal when open', () => {
    render(<GlobalSearch />);

    expect(screen.getByPlaceholderText('Buscar em todos os dashboards...')).toBeInTheDocument();
  });

  it('does not render when closed', () => {
    (useAppStore as unknown as jest.Mock).mockImplementation((selector) =>
      selector({
        searchOpen: false,
        setSearchOpen: jest.fn(),
      })
    );

    const { container } = render(<GlobalSearch />);
    expect(container.firstChild).toBeNull();
  });

  it('shows results when typing', async () => {
    render(<GlobalSearch />);

    const input = screen.getByPlaceholderText('Buscar em todos os dashboards...');
    fireEvent.change(input, { target: { value: 'geral' } });

    await waitFor(() => {
      expect(screen.getByText('Dashboard Geral')).toBeInTheDocument();
    });
  });

  it('shows message for short queries', () => {
    render(<GlobalSearch />);

    expect(screen.getByText('Digite pelo menos 3 caracteres para buscar')).toBeInTheDocument();
  });

  it('closes when X button is clicked', () => {
    const setSearchOpen = jest.fn();
    (useAppStore as unknown as jest.Mock).mockImplementation((selector) =>
      selector({
        searchOpen: true,
        setSearchOpen,
      })
    );

    render(<GlobalSearch />);

    const closeButton = screen.getAllByRole('button')[0];
    fireEvent.click(closeButton);

    expect(setSearchOpen).toHaveBeenCalledWith(false);
  });
});
