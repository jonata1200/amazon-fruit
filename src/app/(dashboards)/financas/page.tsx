// src/app/(dashboards)/financas/page.tsx
'use client';

import { lazy, Suspense } from 'react';
import { MainLayout } from '@/components/layouts/main-layout';
import { PeriodSelector } from '@/components/dashboards/period-selector';
import { DashboardSkeleton } from '@/components/dashboards/dashboard-skeleton';
import { useAppInitialization } from '@/lib/hooks/useAppInitialization';
import { LoadingScreen } from '@/components/ui/loading-screen';
import { ErrorBoundary } from '@/components/error-boundary';

const DashboardFinancasContent = lazy(() =>
  import('@/components/dashboards/financas/dashboard-financas-content').then((module) => ({
    default: module.DashboardFinancasContent,
  }))
);

export default function DashboardFinancasPage() {
  const { isReady } = useAppInitialization();

  if (!isReady) {
    return <LoadingScreen message="Inicializando aplicação..." />;
  }

  return (
    <ErrorBoundary title="Erro no Dashboard de Finanças" message="Ocorreu um erro ao carregar o dashboard de finanças.">
      <MainLayout title="Dashboard de Finanças">
        <div className="space-y-6">
          <PeriodSelector />
          <Suspense fallback={<DashboardSkeleton />}>
            <DashboardFinancasContent />
          </Suspense>
        </div>
      </MainLayout>
    </ErrorBoundary>
  );
}
