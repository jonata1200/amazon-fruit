// src/components/dashboards/estoque/dashboard-estoque-content.tsx
'use client';

import { useDashboardEstoque } from '@/lib/hooks/useDashboards';
import { KPICard } from '@/components/dashboards/kpi-card';
import { DataTable } from '@/components/ui/data-table';
import { EmptyState } from '@/components/ui/empty-state';
import { Package, AlertTriangle, TrendingUp } from 'lucide-react';
import { Skeleton } from '@/components/ui/skeleton';
import { formatNumber } from '@/lib/utils';

function DashboardEstoqueSkeleton() {
  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        <Skeleton className="h-32" />
        <Skeleton className="h-32" />
        <Skeleton className="h-32" />
      </div>
      <Skeleton className="h-64 sm:h-96" />
    </div>
  );
}

export function DashboardEstoqueContent() {
  const { data, isLoading, error } = useDashboardEstoque();

  if (isLoading) {
    return <DashboardEstoqueSkeleton />;
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

  const { kpis, low_stock } = data;

  // Preparar dados da tabela
  const tableData = low_stock.map((item) => ({
    produto: item.produto,
    estoque_atual: item.estoque_atual,
    estoque_minimo: item.estoque_minimo,
    status: item.estoque_atual < item.estoque_minimo ? 'Crítico' : 'Atenção',
  }));

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* KPIs */}
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        <KPICard title="Total de Itens" value={kpis.total_items} format="number" icon={Package} />
        <KPICard
          title="Valor Total do Estoque"
          value={kpis.total_value}
          format="currency"
          icon={TrendingUp}
        />
        <KPICard
          title="Itens em Baixa"
          value={kpis.low_stock_count}
          format="number"
          icon={AlertTriangle}
        />
      </div>

      {/* Tabela de Baixo Estoque */}
      <DataTable
        title="Produtos com Baixo Estoque"
        columns={[
          { key: 'produto', header: 'Produto' },
          {
            key: 'estoque_atual',
            header: 'Estoque Atual',
            render: (value) => formatNumber(Number(value)),
          },
          {
            key: 'estoque_minimo',
            header: 'Estoque Mínimo',
            render: (value) => formatNumber(Number(value)),
          },
          {
            key: 'status',
            header: 'Status',
            render: (value) => (
              <span
                className={value === 'Crítico' ? 'text-red-600 font-semibold' : 'text-yellow-600'}
              >
                {String(value)}
              </span>
            ),
          },
        ]}
        data={tableData}
      />
    </div>
  );
}
