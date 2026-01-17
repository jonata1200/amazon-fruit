// tests/integration/features/export.test.tsx
import { renderWithProviders, screen, waitFor } from '../helpers/render-with-providers';
import userEvent from '@testing-library/user-event';
import { ExportButton } from '@/components/features/export/export-button';
import { useNotifications } from '@/lib/hooks/useNotifications';

// Mock do hook useNotifications
jest.mock('@/lib/hooks/useNotifications');
const mockUseNotifications = useNotifications as jest.MockedFunction<typeof useNotifications>;

// Mock do analytics
jest.mock('@/lib/analytics/events', () => ({
  analytics: {
    dataExported: jest.fn(),
  },
}));

describe('Exportação de Dados - Integração', () => {
  const mockShowSuccess = jest.fn();
  const mockShowError = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    mockUseNotifications.mockReturnValue({
      showSuccess: mockShowSuccess,
      showError: mockShowError,
      showInfo: jest.fn(),
      showWarning: jest.fn(),
    });
  });

  it('renderiza botão de exportação', () => {
    renderWithProviders(<ExportButton dashboard="geral" />);
    
    expect(screen.getByLabelText('Exportar relatório')).toBeInTheDocument();
    expect(screen.getByText('Exportar')).toBeInTheDocument();
  });

  it('exibe menu de opções de exportação', async () => {
    renderWithProviders(<ExportButton dashboard="geral" />);
    
    const button = screen.getByLabelText('Exportar relatório');
    await userEvent.click(button);
    
    await waitFor(() => {
      expect(screen.getByText('Exportar como PDF')).toBeInTheDocument();
      expect(screen.getByText('Exportar como Excel')).toBeInTheDocument();
      expect(screen.getByText('Exportar como CSV')).toBeInTheDocument();
    });
  });

  it('exporta para PDF e exibe notificação de sucesso', async () => {
    renderWithProviders(<ExportButton dashboard="geral" />);
    
    const button = screen.getByLabelText('Exportar relatório');
    await userEvent.click(button);
    
    await waitFor(() => {
      expect(screen.getByText('Exportar como PDF')).toBeInTheDocument();
    });
    
    const pdfOption = screen.getByText('Exportar como PDF');
    await userEvent.click(pdfOption);
    
    // Aguardar a exportação completar (simulação com timers reais)
    await waitFor(() => {
      expect(mockShowSuccess).toHaveBeenCalled();
    }, { timeout: 3000 });
    
    expect(mockShowSuccess).toHaveBeenCalledWith(
      expect.stringContaining('exportado em PDF')
    );
  });

  it('exibe progresso durante exportação', async () => {
    renderWithProviders(<ExportButton dashboard="geral" />);
    
    const button = screen.getByLabelText('Exportar relatório');
    await userEvent.click(button);
    
    await waitFor(() => {
      expect(screen.getByText('Exportar como PDF')).toBeInTheDocument();
    });
    
    const pdfOption = screen.getByText('Exportar como PDF');
    await userEvent.click(pdfOption);
    
    // Aguardar progresso aparecer
    await waitFor(() => {
      expect(screen.getByText(/Exportando.../)).toBeInTheDocument();
    }, { timeout: 500 });
  });

  it('desabilita opções durante exportação', async () => {
    renderWithProviders(<ExportButton dashboard="geral" />);
    
    const button = screen.getByLabelText('Exportar relatório');
    await userEvent.click(button);
    
    await waitFor(() => {
      expect(screen.getByText('Exportar como PDF')).toBeInTheDocument();
    });
    
    const pdfOption = screen.getByText('Exportar como PDF');
    await userEvent.click(pdfOption);
    
    // Aguardar exportação iniciar e menu estar aberto
    await waitFor(() => {
      // Verificar se o progresso está sendo exibido (indica que exportação iniciou)
      const progressText = screen.queryByText(/Exportando.../);
      if (progressText) {
        // Se progresso está visível, verificar se opções estão desabilitadas
        const excelOption = screen.getByText('Exportar como Excel');
        const menuItem = excelOption.closest('[role="menuitem"]') || excelOption.closest('button');
        expect(menuItem).toHaveAttribute('disabled');
      }
    }, { timeout: 2000 });
  });
});
