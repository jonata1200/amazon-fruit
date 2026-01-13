// src/types/api.ts

export interface ApiResponse<T = unknown> {
  status: 'success' | 'error';
  data?: T;
  message?: string;
  error?: string;
}

export interface DateRange {
  start: string; // YYYY-MM-DD
  end: string; // YYYY-MM-DD
}

export interface PeriodData {
  start_date: string;
  end_date: string;
}

// Financial Types
export interface FinancialSummary {
  receita: number;
  despesa: number;
  lucro: number;
  variacao_receita?: number;
  variacao_despesa?: number;
  variacao_lucro?: number;
}

// Dashboard Response Types
export interface DashboardGeralResponse {
  status: string;
  period: PeriodData;
  financial_summary: FinancialSummary;
  evolution_chart: {
    months: string[];
    receita: number[];
    despesa: number[];
    lucro: number[];
  };
}

export interface DashboardFinancasResponse extends DashboardGeralResponse {
  top_expenses: Record<string, { quantidade?: number; valor?: number }>;
  top_revenues: Record<string, { quantidade?: number; valor?: number }>;
}

export interface DashboardEstoqueResponse {
  status: string;
  period: PeriodData;
  kpis: {
    total_items: number;
    total_value: number;
    low_stock_count: number;
  };
  top_selling: Record<string, { quantidade?: number; valor?: number }>;
  least_selling: Record<string, { quantidade?: number; valor?: number }>;
  low_stock: Array<{
    produto: string;
    estoque_atual: number;
    estoque_minimo: number;
  }>;
}

export interface DashboardPublicoAlvoResponse {
  status: string;
  by_location: Record<string, number>;
  by_gender: Record<string, number>;
  by_channel: Record<string, number>;
}

export interface DashboardFornecedoresResponse {
  status: string;
  top_suppliers: Array<{
    nome: string;
    pontuacao: number;
    estado: string;
  }>;
  bottom_suppliers: Array<{
    nome: string;
    pontuacao: number;
    estado: string;
  }>;
  by_state: Record<string, number>;
}

export interface DashboardRecursosHumanosResponse {
  status: string;
  headcount_by_department: Record<string, number>;
  cost_by_department: Record<string, number>;
  by_role: Record<string, number>;
  hiring_over_time: Record<string, number>;
}

// Alerts
export interface Alert {
  id: string;
  type: 'warning' | 'danger' | 'info' | 'success';
  category: string;
  message: string;
  timestamp?: string;
}

export interface AlertsResponse {
  status: string;
  alerts: Alert[];
  count: number;
}

// Search
export interface SearchResult {
  dashboard: string;
  title: string;
  description: string;
  url: string;
}

export interface SearchResponse {
  status: string;
  query: string;
  results: SearchResult[];
  count: number;
}
