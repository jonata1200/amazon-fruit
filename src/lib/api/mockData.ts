// src/lib/api/mockData.ts
// Dados mockados para desenvolvimento quando a API não está disponível

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
  FinancialSummary,
} from '@/types/api';

// Função para gerar dados mensais variados baseado no ano
function generateMonthlyData(year: number, baseMultiplier: number = 1) {
  const months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
  const receita: number[] = [];
  const despesa: number[] = [];
  const lucro: number[] = [];

  months.forEach((_, index) => {
    // Variação sazonal + crescimento ao longo do ano
    const seasonality = 1 + 0.1 * Math.sin((index / 12) * 2 * Math.PI);
    const growth = 1 + (index / 12) * 0.05 * baseMultiplier;
    const multiplier = seasonality * growth * baseMultiplier;

    const baseRevenue = 500000 * multiplier;
    const baseExpense = 300000 * multiplier;
    const revenue = baseRevenue + (Math.random() * 100000 - 50000);
    const expense = baseExpense + (Math.random() * 80000 - 40000);
    const profit = revenue - expense;

    receita.push(Math.round(revenue));
    despesa.push(Math.round(expense));
    lucro.push(Math.round(profit));
  });

  return { months, receita, despesa, lucro };
}

// Função para gerar dados financeiros baseados no período
function generateFinancialData(year: number, dateRange: DateRange): FinancialSummary {
  const multiplier = year === 2024 ? 1 : year === 2025 ? 1.15 : 1.3;
  const baseRevenue = 6000000 * multiplier;
  const baseExpense = 3600000 * multiplier;

  return {
    receita: Math.round(baseRevenue + Math.random() * 500000),
    despesa: Math.round(baseExpense + Math.random() * 300000),
    lucro: Math.round((baseRevenue - baseExpense) + Math.random() * 200000),
    variacao_receita: Math.round((Math.random() * 10 - 2) * 100) / 100,
    variacao_despesa: Math.round((Math.random() * 8 - 1) * 100) / 100,
    variacao_lucro: Math.round((Math.random() * 12 - 1) * 100) / 100,
  };
}

export const mockDataService = {
  getDateRange: () => {
    return {
      min_date: '2024-01-01',
      max_date: '2026-12-31',
    };
  },

  getDashboardGeral: (dateRange: DateRange): DashboardGeralResponse => {
    const startYear = parseInt(dateRange.start.substring(0, 4));
    const endYear = parseInt(dateRange.end.substring(0, 4));
    const year = startYear || 2024;
    
    const financialSummary = generateFinancialData(year, dateRange);
    const monthlyData = generateMonthlyData(year, year === 2024 ? 1 : year === 2025 ? 1.15 : 1.3);

    return {
      status: 'success',
      period: {
        start_date: dateRange.start,
        end_date: dateRange.end,
      },
      financial_summary: financialSummary,
      evolution_chart: monthlyData,
    };
  },

  getDashboardFinancas: (dateRange: DateRange): DashboardFinancasResponse => {
    const geral = mockDataService.getDashboardGeral(dateRange);
    const startYear = parseInt(dateRange.start.substring(0, 4));
    const multiplier = startYear === 2024 ? 1 : startYear === 2025 ? 1.15 : 1.3;

    return {
      ...geral,
      top_expenses: {
        'Salários': { valor: Math.round(1800000 * multiplier) },
        'Aluguel': { valor: Math.round(360000 * multiplier) },
        'Marketing': { valor: Math.round(540000 * multiplier) },
        'Logística': { valor: Math.round(420000 * multiplier) },
        'Manutenção': { valor: Math.round(180000 * multiplier) },
      },
      top_revenues: {
        'Vendas Online': { quantidade: Math.round(45000 * multiplier), valor: Math.round(3600000 * multiplier) },
        'Vendas Físicas': { quantidade: Math.round(28000 * multiplier), valor: Math.round(2400000 * multiplier) },
        'Assinaturas': { quantidade: Math.round(12000 * multiplier), valor: Math.round(1800000 * multiplier) },
      },
    };
  },

  getDashboardEstoque: (dateRange: DateRange): DashboardEstoqueResponse => {
    const startYear = parseInt(dateRange.start.substring(0, 4));
    const multiplier = startYear === 2024 ? 1 : startYear === 2025 ? 1.15 : 1.3;

    return {
      status: 'success',
      period: {
        start_date: dateRange.start,
        end_date: dateRange.end,
      },
      kpis: {
        total_items: Math.round(1250 * multiplier),
        total_value: Math.round(4500000 * multiplier),
        low_stock_count: Math.round(12 + Math.random() * 8),
      },
      top_selling: {
        'Maçã Gala': { quantidade: Math.round(12500 * multiplier), valor: Math.round(375000 * multiplier) },
        'Banana Prata': { quantidade: Math.round(9800 * multiplier), valor: Math.round(196000 * multiplier) },
        'Laranja Lima': { quantidade: Math.round(8500 * multiplier), valor: Math.round(255000 * multiplier) },
        'Uva Itália': { quantidade: Math.round(6200 * multiplier), valor: Math.round(434000 * multiplier) },
        'Manga Palmer': { quantidade: Math.round(4800 * multiplier), valor: Math.round(288000 * multiplier) },
      },
      least_selling: {
        'Carambola': { quantidade: Math.round(120 * multiplier), valor: Math.round(9600 * multiplier) },
        'Acerola': { quantidade: Math.round(180 * multiplier), valor: Math.round(10800 * multiplier) },
        'Pitaya': { quantidade: Math.round(95 * multiplier), valor: Math.round(19000 * multiplier) },
      },
      low_stock: [
        { produto: 'Carambola', estoque_atual: 15, estoque_minimo: 50 },
        { produto: 'Acerola', estoque_atual: 28, estoque_minimo: 100 },
        { produto: 'Pitaya', estoque_atual: 12, estoque_minimo: 40 },
        { produto: 'Lichia', estoque_atual: 35, estoque_minimo: 80 },
      ],
    };
  },

  getDashboardPublicoAlvo: (): DashboardPublicoAlvoResponse => {
    return {
      status: 'success',
      by_location: {
        'São Paulo': 125000,
        'Rio de Janeiro': 85000,
        'Belo Horizonte': 62000,
        'Curitiba': 48000,
        'Porto Alegre': 42000,
        'Recife': 38000,
        'Brasília': 35000,
        'Salvador': 32000,
      },
      by_gender: {
        'Feminino': 245000,
        'Masculino': 195000,
        'Outros': 18000,
      },
      by_channel: {
        'E-commerce': 185000,
        'Loja Física': 125000,
        'App Mobile': 98000,
        'Marketplace': 32000,
      },
    };
  },

  getDashboardFornecedores: (): DashboardFornecedoresResponse => {
    return {
      status: 'success',
      top_suppliers: [
        { nome: 'Frutas do Vale Ltda', pontuacao: 9.8, estado: 'SP' },
        { nome: 'Agricultura Sustentável S.A.', pontuacao: 9.5, estado: 'MG' },
        { nome: 'Fazenda Primavera', pontuacao: 9.2, estado: 'RS' },
        { nome: 'Produtos Orgânicos Brasil', pontuacao: 9.0, estado: 'PR' },
        { nome: 'Distribuidora Frutas & Cia', pontuacao: 8.8, estado: 'SC' },
      ],
      bottom_suppliers: [
        { nome: 'Frutícola Norte', pontuacao: 5.2, estado: 'BA' },
        { nome: 'Agro Distribuidora', pontuacao: 5.8, estado: 'CE' },
        { nome: 'Mercado Frutas Express', pontuacao: 6.1, estado: 'PE' },
      ],
      by_state: {
        'SP': 125,
        'MG': 85,
        'RS': 72,
        'PR': 68,
        'SC': 55,
        'RJ': 48,
        'BA': 35,
        'CE': 28,
      },
    };
  },

  getDashboardRecursosHumanos: (): DashboardRecursosHumanosResponse => {
    return {
      status: 'success',
      headcount_by_department: {
        'Vendas': 85,
        'Operações': 62,
        'TI': 28,
        'RH': 15,
        'Financeiro': 22,
        'Marketing': 18,
        'Logística': 45,
        'Atendimento': 35,
      },
      cost_by_department: {
        'Vendas': 4250000,
        'Operações': 3100000,
        'TI': 2800000,
        'RH': 900000,
        'Financeiro': 1320000,
        'Marketing': 1440000,
        'Logística': 2250000,
        'Atendimento': 1750000,
      },
      by_role: {
        'Analista': 95,
        'Coordenador': 48,
        'Gerente': 28,
        'Diretor': 8,
        'Assistente': 62,
        'Especialista': 35,
      },
      hiring_over_time: {
        '2024-01': 8,
        '2024-02': 5,
        '2024-03': 12,
        '2024-04': 6,
        '2024-05': 10,
        '2024-06': 7,
        '2024-07': 9,
        '2024-08': 11,
        '2024-09': 8,
        '2024-10': 6,
        '2024-11': 9,
        '2024-12': 7,
      },
    };
  },

  getAlerts: (): AlertsResponse => {
    return {
      status: 'success',
      alerts: [
        {
          id: '1',
          type: 'warning',
          category: 'Estoque',
          message: 'Estoque baixo: Carambola (15 unidades)',
          timestamp: new Date().toISOString(),
        },
        {
          id: '2',
          type: 'info',
          category: 'Financeiro',
          message: 'Meta de vendas alcançada em 95%',
          timestamp: new Date().toISOString(),
        },
        {
          id: '3',
          type: 'success',
          category: 'RH',
          message: '5 novas contratações este mês',
          timestamp: new Date().toISOString(),
        },
      ],
      count: 3,
    };
  },

  search: (query: string): SearchResponse => {
    const results = [];
    const dashboards = [
      { id: 'geral', title: 'Dashboard Geral', description: 'Visão geral do negócio' },
      { id: 'financas', title: 'Dashboard de Finanças', description: 'Análise financeira detalhada' },
      { id: 'estoque', title: 'Dashboard de Estoque', description: 'Controle de produtos e estoque' },
      { id: 'publico-alvo', title: 'Dashboard de Público-Alvo', description: 'Segmentação e análise demográfica' },
      { id: 'fornecedores', title: 'Dashboard de Fornecedores', description: 'Ranking e avaliação de fornecedores' },
      { id: 'recursos-humanos', title: 'Dashboard de RH', description: 'Headcount e custos de RH' },
    ];

    const queryLower = query.toLowerCase();
    dashboards.forEach((dashboard) => {
      if (
        dashboard.title.toLowerCase().includes(queryLower) ||
        dashboard.description.toLowerCase().includes(queryLower) ||
        dashboard.id.toLowerCase().includes(queryLower)
      ) {
        results.push({
          dashboard: dashboard.id,
          title: dashboard.title,
          description: dashboard.description,
          url: `/${dashboard.id}`,
        });
      }
    });

    return {
      status: 'success',
      query,
      results,
      count: results.length,
    };
  },
};