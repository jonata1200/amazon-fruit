// src/components/features/__tests__/alerts-panel.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { AlertsPanel } from '../alerts/alerts-panel';
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

describe('AlertsPanel', () => {
  beforeEach(() => {
    (useAppStore as unknown as jest.Mock).mockImplementation((selector) =>
      selector({
        alertsOpen: true,
        toggleAlerts: jest.fn(),
      })
    );

    (useAlerts as jest.Mock).mockReturnValue({
      data: {
        alerts: [
          {
            id: '1',
            type: 'warning',
            category: 'Estoque',
            message: 'Produto com estoque baixo',
            timestamp: new Date().toISOString(),
          },
        ],
        count: 1,
      },
      isLoading: false,
    });
  });

  it('renders alerts panel when open', () => {
    render(<AlertsPanel />);

    expect(screen.getByText('Alertas do Sistema')).toBeInTheDocument();
  });

  it('does not render when closed', () => {
    (useAppStore as unknown as jest.Mock).mockImplementation((selector) =>
      selector({
        alertsOpen: false,
        toggleAlerts: jest.fn(),
      })
    );

    const { container } = render(<AlertsPanel />);
    expect(container.firstChild).toBeNull();
  });

  it('displays alerts', () => {
    render(<AlertsPanel />);

    expect(screen.getByText('Estoque')).toBeInTheDocument();
    expect(screen.getByText('Produto com estoque baixo')).toBeInTheDocument();
  });

  it('shows empty state when no alerts', () => {
    (useAlerts as jest.Mock).mockReturnValue({
      data: { alerts: [], count: 0 },
      isLoading: false,
    });

    render(<AlertsPanel />);

    expect(screen.getByText('Nenhum alerta no momento')).toBeInTheDocument();
  });

  it('closes when X button is clicked', () => {
    const toggleAlerts = jest.fn();
    (useAppStore as unknown as jest.Mock).mockImplementation((selector) =>
      selector({
        alertsOpen: true,
        toggleAlerts,
      })
    );

    render(<AlertsPanel />);

    const closeButton = screen.getByRole('button');
    fireEvent.click(closeButton);

    expect(toggleAlerts).toHaveBeenCalled();
  });

  it('displays alert count in footer', () => {
    render(<AlertsPanel />);

    expect(screen.getByText(/Total: 1 alerta/)).toBeInTheDocument();
  });
});
