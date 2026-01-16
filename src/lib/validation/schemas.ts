// src/lib/validation/schemas.ts
import { z } from 'zod';

/**
 * Schemas de validação Zod para dados da API
 */

// Schema para DashboardId
export const dashboardIdSchema = z.enum([
  'geral',
  'financas',
  'estoque',
  'publico-alvo',
  'fornecedores',
  'recursos-humanos',
]);

export type DashboardIdEnum = z.infer<typeof dashboardIdSchema>;

// Schema para ISODate
export const isoDateSchema = z.string().regex(/^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d{3})?Z?)?$/, {
  message: 'Invalid ISO date format',
});

// Schema para DateRange
export const dateRangeSchema = z.object({
  start: isoDateSchema,
  end: isoDateSchema,
}).refine((data) => new Date(data.start) <= new Date(data.end), {
  message: 'Start date must be before or equal to end date',
  path: ['start'],
});

// Schema para KPI
export const kpiSchema = z.object({
  label: z.string(),
  value: z.union([z.number(), z.string()]),
  change: z.number().optional(),
  changeType: z.enum(['increase', 'decrease', 'neutral']).optional(),
  format: z.enum(['currency', 'number', 'percentage']).optional(),
});

// Schema para dados do dashboard geral
export const financialSummarySchema = z.object({
  receita: z.number(),
  despesa: z.number(),
  lucro: z.number(),
  variacao_receita: z.number().nullable(),
  variacao_despesa: z.number().nullable(),
  variacao_lucro: z.number().nullable(),
});

export const evolutionChartSchema = z.object({
  months: z.array(z.string()),
  receita: z.array(z.number()),
  despesa: z.array(z.number()),
  lucro: z.array(z.number()),
});

export const dashboardGeralSchema = z.object({
  financial_summary: financialSummarySchema,
  evolution_chart: evolutionChartSchema,
});

// Schema para alertas
export const alertTypeSchema = z.enum(['warning', 'danger', 'info', 'success']);

export const alertSchema = z.object({
  id: z.string(),
  type: alertTypeSchema,
  category: z.string(),
  message: z.string(),
  timestamp: z.string().optional(),
});

export const alertsResponseSchema = z.object({
  alerts: z.array(alertSchema),
  count: z.number(),
});

// Schema para período
export const periodSchema = z.enum([
  'today',
  'yesterday',
  'last7days',
  'last30days',
  'last90days',
  'thisMonth',
  'lastMonth',
  'thisYear',
  'lastYear',
  'custom',
]);

/**
 * Helper functions para validação
 */
export function validateDashboardId(id: unknown): id is DashboardIdEnum {
  return dashboardIdSchema.safeParse(id).success;
}

export function validateDateRange(range: unknown): range is z.infer<typeof dateRangeSchema> {
  return dateRangeSchema.safeParse(range).success;
}

export function validateDashboardGeral(data: unknown): data is z.infer<typeof dashboardGeralSchema> {
  return dashboardGeralSchema.safeParse(data).success;
}

export function validateAlertsResponse(data: unknown): data is z.infer<typeof alertsResponseSchema> {
  return alertsResponseSchema.safeParse(data).success;
}
