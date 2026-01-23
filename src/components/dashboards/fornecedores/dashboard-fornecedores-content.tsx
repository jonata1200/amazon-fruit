// src/components/dashboards/fornecedores/dashboard-fornecedores-content.tsx
'use client';

import { useDashboardFornecedores } from '@/lib/hooks/useDashboards';
import { DataTable } from '@/components/ui/data-table';
import { PieChart } from '@/components/charts/pie-chart';
import { EmptyState } from '@/components/ui/empty-state';
import { Skeleton } from '@/components/ui/skeleton';
import { formatNumber } from '@/lib/utils';

function DashboardFornecedoresSkeleton() {
  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="grid gap-4 sm:gap-6 grid-cols-1 lg:grid-cols-2">
        <Skeleton className="h-64 sm:h-96" />
        <Skeleton className="h-64 sm:h-96" />
      </div>
      <Skeleton className="h-64 sm:h-96" />
    </div>
  );
}

export function DashboardFornecedoresContent() {
  const { data, isLoading, error } = useDashboardFornecedores();

  if (isLoading) {
    return <DashboardFornecedoresSkeleton />;
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

  const { top_suppliers, bottom_suppliers, by_state } = data;

  // Preparar dados por estado
  const stateData = Object.entries(by_state).map(([estado, count]) => ({
    name: estado,
    value: count as number,
  }));

  const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Tabelas de Top e Bottom */}
      <div className="grid gap-4 sm:gap-6 grid-cols-1 lg:grid-cols-2">
        <DataTable
          title="🏆 Top 5 Fornecedores"
          columns={[
            { key: 'nome', header: 'Nome' },
            {
              key: 'pontuacao',
              header: 'Pontuação',
              render: (value) => formatNumber(Number(value)),
            },
            { key: 'estado', header: 'Estado' },
          ]}
          data={top_suppliers}
        />
        <DataTable
          title="⚠️ Fornecedores em Atenção"
          columns={[
            { key: 'nome', header: 'Nome' },
            {
              key: 'pontuacao',
              header: 'Pontuação',
              render: (value) => (
                <span className="text-red-600">{formatNumber(Number(value))}</span>
              ),
            },
            { key: 'estado', header: 'Estado' },
          ]}
          data={bottom_suppliers}
        />
      </div>

      {/* Gráfico de Distribuição por Estado */}
      <PieChart
        title="Distribuição de Fornecedores por Estado"
        data={stateData}
        dataKey="value"
        nameKey="name"
        colors={colors}
        height={300}
      />
    </div>
  );
}
