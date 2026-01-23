// src/components/dashboards/recursos-humanos/dashboard-rh-content.tsx
'use client';

import { useDashboardRecursosHumanos } from '@/lib/hooks/useDashboards';
import { BarChart } from '@/components/charts/bar-chart';
import { PieChart } from '@/components/charts/pie-chart';
import { LineChart } from '@/components/charts/line-chart';
import { EmptyState } from '@/components/ui/empty-state';
import { Skeleton } from '@/components/ui/skeleton';

function DashboardRHSkeleton() {
  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="grid gap-4 sm:gap-6 grid-cols-1 lg:grid-cols-2">
        <Skeleton className="h-64 sm:h-96" />
        <Skeleton className="h-64 sm:h-96" />
      </div>
      <div className="grid gap-4 sm:gap-6 grid-cols-1 lg:grid-cols-2">
        <Skeleton className="h-64 sm:h-96" />
        <Skeleton className="h-64 sm:h-96" />
      </div>
    </div>
  );
}

export function DashboardRHContent() {
  const { data, isLoading, error } = useDashboardRecursosHumanos();

  if (isLoading) {
    return <DashboardRHSkeleton />;
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
    return <EmptyState title="Sem dados disponíveis" description="Não há dados disponíveis." />;
  }

  const { headcount_by_department, cost_by_department, by_role, hiring_over_time } = data;

  // Preparar dados
  const headcountData = Object.entries(headcount_by_department).map(([dept, count]) => ({
    departamento: dept,
    funcionarios: count as number,
  }));

  const costData = Object.entries(cost_by_department).map(([dept, cost]) => ({
    departamento: dept,
    custo: cost as number,
  }));

  const roleData = Object.entries(by_role).map(([role, count]) => ({
    name: role,
    value: count as number,
  }));

  const hiringData = Object.entries(hiring_over_time).map(([periodo, count]) => ({
    periodo,
    contratacoes: count as number,
  }));

  const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Headcount e Custo por Departamento */}
      <div className="grid gap-4 sm:gap-6 grid-cols-1 lg:grid-cols-2">
        <BarChart
          title="Funcionários por Departamento"
          data={headcountData}
          xAxisKey="departamento"
          bars={[
            {
              dataKey: 'funcionarios',
              name: 'Funcionários',
              color: '#3b82f6',
            },
          ]}
          height={300}
        />
        <BarChart
          title="Custo por Departamento"
          data={costData}
          xAxisKey="departamento"
          bars={[{ dataKey: 'custo', name: 'Custo (R$)', color: '#10b981' }]}
          height={300}
        />
      </div>

      {/* Distribuição por Cargo e Contratações */}
      <div className="grid gap-4 sm:gap-6 grid-cols-1 lg:grid-cols-2">
        <PieChart
          title="Distribuição por Cargo"
          data={roleData}
          dataKey="value"
          nameKey="name"
          colors={colors}
          height={300}
        />
        <LineChart
          title="Contratações ao Longo do Tempo"
          data={hiringData}
          xAxisKey="periodo"
          lines={[
            {
              dataKey: 'contratacoes',
              name: 'Contratações',
              color: '#8b5cf6',
            },
          ]}
          height={300}
        />
      </div>
    </div>
  );
}
