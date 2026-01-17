// tests/unit/lib/validation/schemas.test.ts
import {
  dashboardIdSchema,
  isoDateSchema,
  dateRangeSchema,
  kpiSchema,
  financialSummarySchema,
  evolutionChartSchema,
  dashboardGeralSchema,
  alertTypeSchema,
  alertSchema,
  alertsResponseSchema,
  periodSchema,
  validateDashboardId,
  validateDateRange,
  validateDashboardGeral,
  validateAlertsResponse,
} from '@/lib/validation/schemas';

describe('Validation Schemas', () => {
  describe('dashboardIdSchema', () => {
    it('validates valid dashboard IDs', () => {
      expect(dashboardIdSchema.safeParse('geral').success).toBe(true);
      expect(dashboardIdSchema.safeParse('financas').success).toBe(true);
      expect(dashboardIdSchema.safeParse('estoque').success).toBe(true);
    });

    it('rejects invalid dashboard IDs', () => {
      expect(dashboardIdSchema.safeParse('invalid').success).toBe(false);
      expect(dashboardIdSchema.safeParse('').success).toBe(false);
    });
  });

  describe('isoDateSchema', () => {
    it('validates valid ISO dates', () => {
      expect(isoDateSchema.safeParse('2024-01-15').success).toBe(true);
      expect(isoDateSchema.safeParse('2024-01-15T12:00:00Z').success).toBe(true);
    });

    it('rejects invalid date formats', () => {
      expect(isoDateSchema.safeParse('2024/01/15').success).toBe(false);
      expect(isoDateSchema.safeParse('invalid').success).toBe(false);
    });
  });

  describe('dateRangeSchema', () => {
    it('validates valid date range', () => {
      const validRange = {
        start: '2024-01-01',
        end: '2024-12-31',
      };
      expect(dateRangeSchema.safeParse(validRange).success).toBe(true);
    });

    it('rejects when start is after end', () => {
      const invalidRange = {
        start: '2024-12-31',
        end: '2024-01-01',
      };
      expect(dateRangeSchema.safeParse(invalidRange).success).toBe(false);
    });

    it('accepts when start equals end', () => {
      const range = {
        start: '2024-01-15',
        end: '2024-01-15',
      };
      expect(dateRangeSchema.safeParse(range).success).toBe(true);
    });
  });

  describe('kpiSchema', () => {
    it('validates valid KPI', () => {
      const validKPI = {
        label: 'Receita',
        value: 1000,
        change: 10,
        changeType: 'increase' as const,
        format: 'currency' as const,
      };
      expect(kpiSchema.safeParse(validKPI).success).toBe(true);
    });

    it('validates KPI with string value', () => {
      const kpi = {
        label: 'Status',
        value: 'active',
      };
      expect(kpiSchema.safeParse(kpi).success).toBe(true);
    });

    it('validates KPI without optional fields', () => {
      const kpi = {
        label: 'Total',
        value: 1000,
      };
      expect(kpiSchema.safeParse(kpi).success).toBe(true);
    });
  });

  describe('financialSummarySchema', () => {
    it('validates valid financial summary', () => {
      const summary = {
        receita: 100000,
        despesa: 60000,
        lucro: 40000,
        variacao_receita: 15,
        variacao_despesa: 10,
        variacao_lucro: 20,
      };
      expect(financialSummarySchema.safeParse(summary).success).toBe(true);
    });

    it('validates with null variations', () => {
      const summary = {
        receita: 100000,
        despesa: 60000,
        lucro: 40000,
        variacao_receita: null,
        variacao_despesa: null,
        variacao_lucro: null,
      };
      expect(financialSummarySchema.safeParse(summary).success).toBe(true);
    });
  });

  describe('evolutionChartSchema', () => {
    it('validates valid evolution chart data', () => {
      const chart = {
        months: ['Jan', 'Fev', 'Mar'],
        receita: [1000, 1500, 1200],
        despesa: [500, 600, 550],
        lucro: [500, 900, 650],
      };
      expect(evolutionChartSchema.safeParse(chart).success).toBe(true);
    });
  });

  describe('dashboardGeralSchema', () => {
    it('validates valid dashboard geral data', () => {
      const data = {
        financial_summary: {
          receita: 100000,
          despesa: 60000,
          lucro: 40000,
          variacao_receita: 15,
          variacao_despesa: 10,
          variacao_lucro: 20,
        },
        evolution_chart: {
          months: ['Jan', 'Fev'],
          receita: [1000, 1500],
          despesa: [500, 600],
          lucro: [500, 900],
        },
      };
      expect(dashboardGeralSchema.safeParse(data).success).toBe(true);
    });
  });

  describe('alertSchema', () => {
    it('validates valid alert', () => {
      const alert = {
        id: '1',
        type: 'warning' as const,
        category: 'Estoque',
        message: 'Produto com estoque baixo',
        timestamp: '2024-01-15T12:00:00Z',
      };
      expect(alertSchema.safeParse(alert).success).toBe(true);
    });

    it('validates alert without timestamp', () => {
      const alert = {
        id: '1',
        type: 'danger' as const,
        category: 'Financeiro',
        message: 'Erro crítico',
      };
      expect(alertSchema.safeParse(alert).success).toBe(true);
    });
  });

  describe('alertsResponseSchema', () => {
    it('validates valid alerts response', () => {
      const response = {
        alerts: [
          {
            id: '1',
            type: 'warning' as const,
            category: 'Estoque',
            message: 'Test',
          },
        ],
        count: 1,
      };
      expect(alertsResponseSchema.safeParse(response).success).toBe(true);
    });
  });

  describe('periodSchema', () => {
    it('validates valid periods', () => {
      expect(periodSchema.safeParse('today').success).toBe(true);
      expect(periodSchema.safeParse('last7days').success).toBe(true);
      expect(periodSchema.safeParse('custom').success).toBe(true);
    });

    it('rejects invalid periods', () => {
      expect(periodSchema.safeParse('invalid').success).toBe(false);
    });
  });

  describe('Helper Functions', () => {
    it('validateDashboardId returns true for valid IDs', () => {
      expect(validateDashboardId('geral')).toBe(true);
      expect(validateDashboardId('financas')).toBe(true);
    });

    it('validateDashboardId returns false for invalid IDs', () => {
      expect(validateDashboardId('invalid')).toBe(false);
    });

    it('validateDateRange returns true for valid ranges', () => {
      expect(validateDateRange({ start: '2024-01-01', end: '2024-12-31' })).toBe(true);
    });

    it('validateDateRange returns false for invalid ranges', () => {
      expect(validateDateRange({ start: '2024-12-31', end: '2024-01-01' })).toBe(false);
    });

    it('validateDashboardGeral returns true for valid data', () => {
      const data = {
        financial_summary: {
          receita: 100000,
          despesa: 60000,
          lucro: 40000,
          variacao_receita: 15,
          variacao_despesa: 10,
          variacao_lucro: 20,
        },
        evolution_chart: {
          months: ['Jan'],
          receita: [1000],
          despesa: [500],
          lucro: [500],
        },
      };
      expect(validateDashboardGeral(data)).toBe(true);
    });

    it('validateAlertsResponse returns true for valid response', () => {
      const response = {
        alerts: [
          {
            id: '1',
            type: 'warning' as const,
            category: 'Test',
            message: 'Test',
          },
        ],
        count: 1,
      };
      expect(validateAlertsResponse(response)).toBe(true);
    });
  });
});
