// src/lib/api/services.ts
import { apiClient } from './client';
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

export const dashboardService = {
  // Get date range available
  getDateRange: async () => {
    return apiClient.get<{ min_date: string; max_date: string }>('/api/data/date-range');
  },

  // Dashboard Geral
  getDashboardGeral: async (dateRange: DateRange) => {
    return apiClient.get<DashboardGeralResponse>('/api/dashboard/geral', {
      params: {
        start_date: dateRange.start,
        end_date: dateRange.end,
      },
    });
  },

  // Dashboard Financas
  getDashboardFinancas: async (dateRange: DateRange) => {
    return apiClient.get<DashboardFinancasResponse>('/api/dashboard/financas', {
      params: {
        start_date: dateRange.start,
        end_date: dateRange.end,
      },
    });
  },

  // Dashboard Estoque
  getDashboardEstoque: async (dateRange: DateRange) => {
    return apiClient.get<DashboardEstoqueResponse>('/api/dashboard/estoque', {
      params: {
        start_date: dateRange.start,
        end_date: dateRange.end,
      },
    });
  },

  // Dashboard Público-Alvo
  getDashboardPublicoAlvo: async () => {
    return apiClient.get<DashboardPublicoAlvoResponse>('/api/dashboard/publico_alvo');
  },

  // Dashboard Fornecedores
  getDashboardFornecedores: async () => {
    return apiClient.get<DashboardFornecedoresResponse>('/api/dashboard/fornecedores');
  },

  // Dashboard Recursos Humanos
  getDashboardRecursosHumanos: async () => {
    return apiClient.get<DashboardRecursosHumanosResponse>('/api/dashboard/recursos_humanos');
  },
};

export const alertService = {
  getAlerts: async () => {
    return apiClient.get<AlertsResponse>('/api/alerts');
  },
};

export const searchService = {
  search: async (query: string) => {
    return apiClient.get<SearchResponse>('/api/search', {
      params: { q: query },
    });
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
