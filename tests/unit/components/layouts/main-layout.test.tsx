// tests/unit/components/layouts/main-layout.test.tsx
import { render, screen } from '@testing-library/react';
import { MainLayout } from '@/components/layouts/main-layout';
import { useAppStore } from '@/store';

// Mock do store
jest.mock('@/store', () => ({
  useAppStore: jest.fn(),
}));

// Mock dos componentes filhos
jest.mock('@/components/layouts/sidebar', () => ({
  Sidebar: () => <div data-testid="sidebar">Sidebar</div>,
}));

jest.mock('@/components/layouts/header', () => ({
  Header: ({ title }: { title: string }) => <div data-testid="header">{title}</div>,
}));

jest.mock('@/components/layouts/footer', () => ({
  Footer: () => <div data-testid="footer">Footer</div>,
}));

jest.mock('@/components/features/alerts/alerts-panel', () => ({
  AlertsPanel: () => <div data-testid="alerts-panel">AlertsPanel</div>,
}));

jest.mock('@/components/features/search/global-search', () => ({
  GlobalSearch: () => <div data-testid="global-search">GlobalSearch</div>,
}));

jest.mock('@/lib/hooks/useKeyboardShortcuts', () => ({
  useKeyboardShortcuts: jest.fn(),
}));

describe('MainLayout', () => {
  beforeEach(() => {
    (useAppStore as unknown as jest.Mock).mockImplementation((selector) => {
      if (typeof selector === 'function') {
        return selector({
          sidebarOpen: true,
        });
      }
    });
  });

  it('renders all layout components', () => {
    render(
      <MainLayout title="Test Dashboard">
        <div>Content</div>
      </MainLayout>
    );

    expect(screen.getByTestId('sidebar')).toBeInTheDocument();
    expect(screen.getByTestId('header')).toBeInTheDocument();
    expect(screen.getByTestId('footer')).toBeInTheDocument();
    expect(screen.getByTestId('alerts-panel')).toBeInTheDocument();
    expect(screen.getByTestId('global-search')).toBeInTheDocument();
  });

  it('renders children content', () => {
    render(
      <MainLayout title="Test">
        <div>Test Content</div>
      </MainLayout>
    );
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('passes title to Header', () => {
    render(
      <MainLayout title="Dashboard Title">
        <div>Content</div>
      </MainLayout>
    );
    expect(screen.getByText('Dashboard Title')).toBeInTheDocument();
  });

  it('adjusts margin when sidebar is open', () => {
    const { container } = render(
      <MainLayout title="Test">
        <div>Content</div>
      </MainLayout>
    );
    const mainContent = container.querySelector('.lg\\:ml-64');
    expect(mainContent).toBeInTheDocument();
  });

  it('has main content area with correct id', () => {
    const { container } = render(
      <MainLayout title="Test">
        <div>Content</div>
      </MainLayout>
    );
    const main = container.querySelector('#main-content');
    expect(main).toBeInTheDocument();
  });
});
