// src/lib/api/services.ts
import { apiClient } from './client';
import { mockDataService } from './mockData';
import type {
  DashboardGeralResponse,
  DashboardFinancasResponse,
  DashboardEstoqueResponse,
  DashboardPublicoAlvoResponse,
  DashboardFornecedoresResponse,
  DashboardRecursosHumanosResponse,
  AlertsResponse,
  SearchResponse,
  DateRange,
} from '@/types/api';

// Verificar se a API está disponível
const isApiAvailable = () => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  // Em desenvolvimento, usar mock se não houver API configurada ou se for localhost:8000
  if (process.env.NODE_ENV === 'development' && (!apiUrl || apiUrl.includes('localhost:8000'))) {
    return false;
  }
  return true;
};

export const dashboardService = {
  // Get date range available
  getDateRange: async () => {
    if (!isApiAvailable()) {
      return mockDataService.getDateRange();
    }
    try {
      return await apiClient.get<{ min_date: string; max_date: string }>('/api/data/date-range');
    } catch (error) {
      // Se a API falhar, usar dados mock
      return mockDataService.getDateRange();
    }
  },

  // Dashboard Geral
  getDashboardGeral: async (dateRange: DateRange) => {
    if (!isApiAvailable()) {
      return mockDataService.getDashboardGeral(dateRange);
    }
    try {
      return await apiClient.get<DashboardGeralResponse>('/api/dashboard/geral', {
        params: {
          start_date: dateRange.start,
          end_date: dateRange.end,
        },
      });
    } catch (error) {
      return mockDataService.getDashboardGeral(dateRange);
    }
  },

  // Dashboard Financas
  getDashboardFinancas: async (dateRange: DateRange) => {
    if (!isApiAvailable()) {
      return mockDataService.getDashboardFinancas(dateRange);
    }
    try {
      return await apiClient.get<DashboardFinancasResponse>('/api/dashboard/financas', {
        params: {
          start_date: dateRange.start,
          end_date: dateRange.end,
        },
      });
    } catch (error) {
      return mockDataService.getDashboardFinancas(dateRange);
    }
  },

  // Dashboard Estoque
  getDashboardEstoque: async (dateRange: DateRange) => {
    if (!isApiAvailable()) {
      return mockDataService.getDashboardEstoque(dateRange);
    }
    try {
      return await apiClient.get<DashboardEstoqueResponse>('/api/dashboard/estoque', {
        params: {
          start_date: dateRange.start,
          end_date: dateRange.end,
        },
      });
    } catch (error) {
      return mockDataService.getDashboardEstoque(dateRange);
    }
  },

  // Dashboard Público-Alvo
  getDashboardPublicoAlvo: async () => {
    if (!isApiAvailable()) {
      return mockDataService.getDashboardPublicoAlvo();
    }
    try {
      return await apiClient.get<DashboardPublicoAlvoResponse>('/api/dashboard/publico_alvo');
    } catch (error) {
      return mockDataService.getDashboardPublicoAlvo();
    }
  },

  // Dashboard Fornecedores
  getDashboardFornecedores: async () => {
    if (!isApiAvailable()) {
      return mockDataService.getDashboardFornecedores();
    }
    try {
      return await apiClient.get<DashboardFornecedoresResponse>('/api/dashboard/fornecedores');
    } catch (error) {
      return mockDataService.getDashboardFornecedores();
    }
  },

  // Dashboard Recursos Humanos
  getDashboardRecursosHumanos: async () => {
    if (!isApiAvailable()) {
      return mockDataService.getDashboardRecursosHumanos();
    }
    try {
      return await apiClient.get<DashboardRecursosHumanosResponse>('/api/dashboard/recursos_humanos');
    } catch (error) {
      return mockDataService.getDashboardRecursosHumanos();
    }
  },
};

export const alertService = {
  getAlerts: async () => {
    if (!isApiAvailable()) {
      return mockDataService.getAlerts();
    }
    try {
      return await apiClient.get<AlertsResponse>('/api/alerts');
    } catch (error) {
      return mockDataService.getAlerts();
    }
  },
};

export const searchService = {
  search: async (query: string) => {
    if (!isApiAvailable()) {
      return mockDataService.search(query);
    }
    try {
      return await apiClient.get<SearchResponse>('/api/search', {
        params: { q: query },
      });
    } catch (error) {
      return mockDataService.search(query);
    }
  },
};

export const exportService = {
  exportPDF: async (dashboard: string, dateRange: DateRange) => {
    return apiClient.get(`/api/export/pdf/${dashboard}`, {
      params: {
        start_date: dateRange.start,
        end_date: dateRange.end,
      },
      responseType: 'blob',
    });
  },

  exportExcel: async (dashboard: string, dateRange: DateRange) => {
    return apiClient.get(`/api/export/excel/${dashboard}`, {
      params: {
        start_date: dateRange.start,
        end_date: dateRange.end,
      },
      responseType: 'blob',
    });
  },
};
