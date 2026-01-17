// src/components/dashboards/geral/dashboard-geral-content.tsx
'use client';

import { useMemo } from 'react';
import { useDashboardGeral } from '@/lib/hooks/useDashboards';
import { KPICard } from '@/components/dashboards/kpi-card';
import { LineChart } from '@/components/charts/line-chart';
import { EmptyState } from '@/components/ui/empty-state';
import { DollarSign, TrendingUp, TrendingDown } from 'lucide-react';
import { Skeleton } from '@/components/ui/skeleton';

function DashboardGeralSkeleton() {
  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-3">
        <Skeleton className="h-32" />
        <Skeleton className="h-32" />
        <Skeleton className="h-32" />
      </div>
      <Skeleton className="h-96" />
    </div>
  );
}

export function DashboardGeralContent() {
  const { data, isLoading, error } = useDashboardGeral();

  // Preparar dados do gráfico de evolução (memoizado)
  // IMPORTANTE: Todos os hooks devem ser chamados antes de qualquer return condicional
  const chartData = useMemo(
    () => {
      if (!data?.evolution_chart) return [];
      return data.evolution_chart.months.map((month, index) => ({
        mes: month,
        receita: data.evolution_chart.receita[index],
        despesa: data.evolution_chart.despesa[index],
        lucro: data.evolution_chart.lucro[index],
      }));
    },
    [data]
  );

  if (isLoading) {
    return <DashboardGeralSkeleton />;
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

  const { financial_summary } = data;

  return (
    <div className="space-y-6">
      {/* KPIs */}
      <div className="grid gap-4 md:grid-cols-3">
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
          title="Lucro Total"
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
        title="Evolução Financeira"
        data={chartData}
        xAxisKey="mes"
        lines={[
          { dataKey: 'receita', name: 'Receita', color: '#10b981' },
          { dataKey: 'despesa', name: 'Despesa', color: '#ef4444' },
          { dataKey: 'lucro', name: 'Lucro', color: '#3b82f6' },
        ]}
        height={400}
      />
    </div>
  );
}
