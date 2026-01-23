// src/components/dashboards/publico-alvo/dashboard-publico-alvo-content.tsx
'use client';

import { useDashboardPublicoAlvo } from '@/lib/hooks/useDashboards';
import { BarChart } from '@/components/charts/bar-chart';
import { PieChart } from '@/components/charts/pie-chart';
import { EmptyState } from '@/components/ui/empty-state';
import { Skeleton } from '@/components/ui/skeleton';

function DashboardPublicoAlvoSkeleton() {
  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="grid gap-4 sm:gap-6 grid-cols-1 lg:grid-cols-3">
        <Skeleton className="h-64 sm:h-96" />
        <Skeleton className="h-64 sm:h-96" />
        <Skeleton className="h-64 sm:h-96" />
      </div>
    </div>
  );
}

export function DashboardPublicoAlvoContent() {
  const { data, isLoading, error } = useDashboardPublicoAlvo();

  if (isLoading) {
    return <DashboardPublicoAlvoSkeleton />;
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

  const { by_location, by_gender, by_channel } = data;

  // Preparar dados
  const locationData = Object.entries(by_location).map(([local, count]) => ({
    local,
    count: count as number,
  }));

  const genderData = Object.entries(by_gender).map(([genero, count]) => ({
    name: genero,
    value: count as number,
  }));

  const channelData = Object.entries(by_channel).map(([canal, count]) => ({
    name: canal,
    value: count as number,
  }));

  const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Gráficos de Distribuição */}
      <div className="grid gap-4 sm:gap-6 grid-cols-1 lg:grid-cols-3">
        <BarChart
          title="Distribuição por Localização"
          data={locationData}
          xAxisKey="local"
          bars={[{ dataKey: 'count', name: 'Clientes', color: '#3b82f6' }]}
          height={300}
        />
        <PieChart
          title="Distribuição por Gênero"
          data={genderData}
          dataKey="value"
          nameKey="name"
          colors={colors}
          height={300}
        />
        <PieChart
          title="Distribuição por Canal"
          data={channelData}
          dataKey="value"
          nameKey="name"
          colors={colors}
          height={300}
        />
      </div>
    </div>
  );
}
