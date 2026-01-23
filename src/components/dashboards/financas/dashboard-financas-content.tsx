// src/components/dashboards/financas/dashboard-financas-content.tsx
'use client';

import { useDashboardFinancas } from '@/lib/hooks/useDashboards';
import { KPICard } from '@/components/dashboards/kpi-card';
import { LineChart } from '@/components/charts/line-chart';
import { BarChart } from '@/components/charts/bar-chart';
import { EmptyState } from '@/components/ui/empty-state';
import { DollarSign, TrendingUp, TrendingDown } from 'lucide-react';
import { Skeleton } from '@/components/ui/skeleton';

function DashboardFinancasSkeleton() {
  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        {[1, 2, 3].map((i) => (
          <Skeleton key={i} className="h-32" />
        ))}
      </div>
      <Skeleton className="h-64 sm:h-96" />
      <div className="grid gap-4 sm:gap-6 grid-cols-1 lg:grid-cols-2">
        <Skeleton className="h-64 sm:h-80" />
        <Skeleton className="h-64 sm:h-80" />
      </div>
    </div>
  );
}

export function DashboardFinancasContent() {
  const { data, isLoading, error } = useDashboardFinancas();

  if (isLoading) {
    return <DashboardFinancasSkeleton />;
  }

  if (error) {
    return (
      <EmptyState
        title="Erro ao carregar dashboard"
        description="Não foi possível carregar os dados. Tente novamente mais tarde."
      />
    );
  }

  if (!data) {
    return (
      <EmptyState
        title="Sem dados disponíveis"
        description="Não há dados para o período selecionado."
      />
    );
  }

  const { financial_summary, evolution_chart, top_expenses, top_revenues } = data;

  // Preparar dados dos gráficos
  const chartData = evolution_chart.months.map((month, index) => ({
    mes: month,
    receita: evolution_chart.receita[index],
    despesa: evolution_chart.despesa[index],
    lucro: evolution_chart.lucro[index],
  }));

  // Preparar dados de top despesas
  const expensesData = Object.entries(top_expenses).map(([categoria, dados]) => ({
    categoria,
    valor: (dados as { valor?: number }).valor || 0,
  }));

  // Preparar dados de top receitas
  const revenuesData = Object.entries(top_revenues).map(([categoria, dados]) => ({
    categoria,
    valor: (dados as { valor?: number }).valor || 0,
  }));

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* KPIs */}
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        <KPICard
          title="Receita Total"
          value={financial_summary.receita}
          change={financial_summary.variacao_receita}
          changeType={
            financial_summary.variacao_receita && financial_summary.variacao_receita > 0
              ? 'increase'
              : 'decrease'
          }
          format="currency"
          icon={DollarSign}
        />
        <KPICard
          title="Despesa Total"
          value={financial_summary.despesa}
          change={financial_summary.variacao_despesa}
          changeType={
            financial_summary.variacao_despesa && financial_summary.variacao_despesa > 0
              ? 'increase'
              : 'decrease'
          }
          format="currency"
          icon={TrendingDown}
        />
        <KPICard
          title="Lucro"
          value={financial_summary.lucro}
          change={financial_summary.variacao_lucro}
          changeType={
            financial_summary.variacao_lucro && financial_summary.variacao_lucro > 0
              ? 'increase'
              : 'decrease'
          }
          format="currency"
          icon={TrendingUp}
        />
      </div>

      {/* Gráfico de Evolução */}
      <LineChart
        title="Evolução Financeira Mensal"
        data={chartData}
        xAxisKey="mes"
        lines={[
          { dataKey: 'receita', name: 'Receita', color: '#10b981' },
          { dataKey: 'despesa', name: 'Despesa', color: '#ef4444' },
          { dataKey: 'lucro', name: 'Lucro', color: '#3b82f6' },
        ]}
        height={300}
      />

      {/* Gráficos de Top Despesas e Receitas */}
      <div className="grid gap-4 sm:gap-6 grid-cols-1 lg:grid-cols-2">
        <BarChart
          title="Top 5 Despesas"
          data={expensesData}
          xAxisKey="categoria"
          bars={[{ dataKey: 'valor', name: 'Valor', color: '#ef4444' }]}
          layout="vertical"
          height={250}
        />
        <BarChart
          title="Top 5 Receitas"
          data={revenuesData}
          xAxisKey="categoria"
          bars={[{ dataKey: 'valor', name: 'Valor', color: '#10b981' }]}
          layout="vertical"
          height={250}
        />
      </div>
    </div>
  );
}
