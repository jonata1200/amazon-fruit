// src/app/(dashboards)/estoque/page.tsx
'use client';

import { lazy, Suspense } from 'react';
import { MainLayout } from '@/components/layouts/main-layout';
import { PeriodSelector } from '@/components/dashboards/period-selector';
import { DashboardSkeleton } from '@/components/dashboards/dashboard-skeleton';
import { useAppInitialization } from '@/lib/hooks/useAppInitialization';
import { LoadingScreen } from '@/components/ui/loading-screen';
import { ErrorBoundary } from '@/components/error-boundary';

const DashboardEstoqueContent = lazy(() =>
  import('@/components/dashboards/estoque/dashboard-estoque-content').then((module) => ({
    default: module.DashboardEstoqueContent,
  }))
);

export default function DashboardEstoquePage() {
  const { isReady } = useAppInitialization();

  if (!isReady) {
    return <LoadingScreen message="Inicializando aplicação..." />;
  }

  return (
    <ErrorBoundary title="Erro no Dashboard de Estoque" message="Ocorreu um erro ao carregar o dashboard de estoque.">
      <MainLayout title="Dashboard de Estoque">
        <div className="space-y-6">
          <PeriodSelector />
          <Suspense fallback={<DashboardSkeleton />}>
            <DashboardEstoqueContent />
          </Suspense>
        </div>
      </MainLayout>
    </ErrorBoundary>
  );
}
