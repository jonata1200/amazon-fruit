// src/app/(dashboards)/geral/page.tsx
'use client';

import { lazy, Suspense } from 'react';
import { MainLayout } from '@/components/layouts/main-layout';
import { PeriodSelector } from '@/components/dashboards/period-selector';
import { DashboardSkeleton } from '@/components/dashboards/dashboard-skeleton';
import { useAppInitialization } from '@/lib/hooks/useAppInitialization';
import { LoadingScreen } from '@/components/ui/loading-screen';
import { ErrorBoundary } from '@/components/error-boundary';
import { usePageView } from '@/lib/hooks/useAnalytics';

const DashboardGeralContent = lazy(() =>
  import('@/components/dashboards/geral/dashboard-geral-content').then((module) => ({
    default: module.DashboardGeralContent,
  }))
);

export default function DashboardGeralPage() {
  const { isReady } = useAppInitialization();
  usePageView('geral');

  if (!isReady) {
    return <LoadingScreen message="Inicializando aplicação..." />;
  }

  return (
    <ErrorBoundary title="Erro no Dashboard Geral" message="Ocorreu um erro ao carregar o dashboard geral.">
      <MainLayout title="Visão Geral do Negócio">
        <div className="space-y-6">
          <PeriodSelector />
          <Suspense fallback={<DashboardSkeleton />}>
            <DashboardGeralContent />
          </Suspense>
        </div>
      </MainLayout>
    </ErrorBoundary>
  );
}
