// tests/unit/components/features/export-button.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ExportButton } from '@/components/features/export/export-button';

// Mock do hook de notificações
jest.mock('@/lib/hooks/useNotifications', () => ({
  useNotifications: () => ({
    showSuccess: jest.fn(),
    showError: jest.fn(),
  }),
}));

describe('ExportButton', () => {
  it('renders export button', () => {
    render(<ExportButton dashboard="geral" />);

    expect(screen.getByText('Exportar')).toBeInTheDocument();
  });

  it('shows dropdown menu when clicked', () => {
    render(<ExportButton dashboard="geral" />);

    fireEvent.click(screen.getByText('Exportar'));

    expect(screen.getByText('Exportar como PDF')).toBeInTheDocument();
    expect(screen.getByText('Exportar como Excel')).toBeInTheDocument();
    expect(screen.getByText('Exportar como CSV')).toBeInTheDocument();
  });

  it('shows loading state during export', async () => {
    render(<ExportButton dashboard="geral" />);

    fireEvent.click(screen.getByText('Exportar'));
    fireEvent.click(screen.getByText('Exportar como PDF'));

    await waitFor(() => {
      expect(screen.getByText('Exportando...')).toBeInTheDocument();
    });
  });

  it('disables button during export', async () => {
    render(<ExportButton dashboard="geral" />);

    fireEvent.click(screen.getByText('Exportar'));
    fireEvent.click(screen.getByText('Exportar como PDF'));

    await waitFor(() => {
      const button = screen.getByText('Exportando...').closest('button');
      expect(button).toBeDisabled();
    });
  });
});
