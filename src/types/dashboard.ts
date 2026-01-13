// src/types/dashboard.ts

export interface KPI {
  label: string;
  value: number | string;
  change?: number;
  changeType?: 'increase' | 'decrease' | 'neutral';
  format?: 'currency' | 'number' | 'percentage';
}

export interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    color?: string;
  }[];
}

export interface TableData {
  headers: string[];
  rows: (string | number)[][];
}

export type DashboardId =
  | 'geral'
  | 'financas'
  | 'estoque'
  | 'publico-alvo'
  | 'fornecedores'
  | 'recursos-humanos';
