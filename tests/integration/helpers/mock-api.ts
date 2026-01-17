// tests/integration/helpers/mock-api.ts
import { alertService, dashboardService } from '@/lib/api/services';

// Mock dos serviços de API
export const mockAlertService = {
  getAlerts: jest.fn(),
};

export const mockDashboardService = {
  getDashboardGeral: jest.fn(),
  getDashboardFinancas: jest.fn(),
  getDashboardEstoque: jest.fn(),
  getDashboardPublicoAlvo: jest.fn(),
  getDashboardFornecedores: jest.fn(),
  getDashboardRH: jest.fn(),
};

export const mockSearchService = {
  search: jest.fn(),
};

export const mockExportService = {
  exportToPDF: jest.fn(),
  exportToExcel: jest.fn(),
  exportToCSV: jest.fn(),
};

// Dados mock padrão
export const mockAlertsResponse = {
  alerts: [
    {
      id: '1',
      type: 'warning' as const,
      category: 'Estoque',
      message: 'Produto X com estoque baixo',
      timestamp: new Date().toISOString(),
    },
    {
      id: '2',
      type: 'danger' as const,
      category: 'Financeiro',
      message: 'Despesas acima do orçamento',
      timestamp: new Date().toISOString(),
    },
  ],
  count: 2,
};

export const mockDashboardGeralResponse = {
  financial_summary: {
    receita: 100000,
    despesa: 60000,
    lucro: 40000,
    variacao_receita: 15,
    variacao_despesa: 10,
    variacao_lucro: 20,
  },
  evolution_chart: {
    months: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    receita: [80000, 85000, 90000, 95000, 98000, 100000],
    despesa: [50000, 52000, 54000, 56000, 58000, 60000],
    lucro: [30000, 33000, 36000, 39000, 40000, 40000],
  },
};

export const mockSearchResponse = {
  results: [
    { id: 'geral', name: 'Dashboard Geral', type: 'dashboard', href: '/geral' },
    { id: 'financas', name: 'Dashboard Finanças', type: 'dashboard', href: '/financas' },
  ],
  total: 2,
};

// Setup de mocks
export function setupApiMocks() {
  jest.mock('@/lib/api/services', () => ({
    alertService: mockAlertService,
    dashboardService: mockDashboardService,
    searchService: mockSearchService,
    exportService: mockExportService,
  }));

  // Configurar retornos padrão
  mockAlertService.getAlerts.mockResolvedValue(mockAlertsResponse);
  mockDashboardService.getDashboardGeral.mockResolvedValue(mockDashboardGeralResponse);
  mockSearchService.search.mockResolvedValue(mockSearchResponse);
}

// Reset de mocks
export function resetApiMocks() {
  mockAlertService.getAlerts.mockReset();
  mockDashboardService.getDashboardGeral.mockReset();
  mockDashboardService.getDashboardFinancas.mockReset();
  mockDashboardService.getDashboardEstoque.mockReset();
  mockDashboardService.getDashboardPublicoAlvo.mockReset();
  mockDashboardService.getDashboardFornecedores.mockReset();
  mockDashboardService.getDashboardRH.mockReset();
  mockSearchService.search.mockReset();
  mockExportService.exportToPDF.mockReset();
  mockExportService.exportToExcel.mockReset();
  mockExportService.exportToCSV.mockReset();
}
