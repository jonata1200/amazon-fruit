// tests/fixtures/index.ts
/**
 * Fixtures centralizados para testes
 * Reutilize estes dados em múltiplos testes para consistência
 */

// Dados mock de dashboard geral
export const mockDashboardGeralData = {
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

// Dados mock de alertas
export const mockAlertsData = {
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
    {
      id: '3',
      type: 'info' as const,
      category: 'Vendas',
      message: 'Nova promoção disponível',
      timestamp: new Date().toISOString(),
    },
  ],
  count: 3,
};

// Dados mock de KPIs
export const mockKPIData = {
  receita: {
    title: 'Receita',
    value: 100000,
    change: 15,
    changeType: 'increase' as const,
    format: 'currency' as const,
  },
  despesa: {
    title: 'Despesa',
    value: 60000,
    change: 10,
    changeType: 'increase' as const,
    format: 'currency' as const,
  },
  lucro: {
    title: 'Lucro',
    value: 40000,
    change: 20,
    changeType: 'increase' as const,
    format: 'currency' as const,
  },
};

// Dados mock de tabela
export const mockTableData = [
  { id: '1', name: 'Item 1', value: 100, status: 'Ativo' },
  { id: '2', name: 'Item 2', value: 200, status: 'Inativo' },
  { id: '3', name: 'Item 3', value: 300, status: 'Ativo' },
];

export const mockTableColumns = [
  { key: 'name', header: 'Nome' },
  { key: 'value', header: 'Valor' },
  { key: 'status', header: 'Status' },
];

// Factory functions para criar dados de teste
export function createMockAlert(overrides?: Partial<typeof mockAlertsData.alerts[0]>) {
  return {
    id: `alert-${Date.now()}`,
    type: 'info' as const,
    category: 'Test',
    message: 'Test message',
    timestamp: new Date().toISOString(),
    ...overrides,
  };
}

export function createMockKPI(overrides?: Partial<typeof mockKPIData.receita>) {
  return {
    title: 'Test KPI',
    value: 0,
    change: 0,
    changeType: 'neutral' as const,
    format: 'number' as const,
    ...overrides,
  };
}
