// src/app/(dashboards)/publico-alvo/page.tsx
'use client';

import { lazy, Suspense } from 'react';
import { MainLayout } from '@/components/layouts/main-layout';
import { DashboardSkeleton } from '@/components/dashboards/dashboard-skeleton';
import { useAppInitialization } from '@/lib/hooks/useAppInitialization';
import { LoadingScreen } from '@/components/ui/loading-screen';
import { ErrorBoundary } from '@/components/error-boundary';

const DashboardPublicoAlvoContent = lazy(() =>
  import('@/components/dashboards/publico-alvo/dashboard-publico-alvo-content').then((module) => ({
    default: module.DashboardPublicoAlvoContent,
  }))
);

export default function DashboardPublicoAlvoPage() {
  const { isReady } = useAppInitialization();

  if (!isReady) {
    return <LoadingScreen message="Inicializando aplicação..." />;
  }

  return (
    <ErrorBoundary title="Erro no Dashboard de Público-Alvo" message="Ocorreu um erro ao carregar o dashboard de público-alvo.">
      <MainLayout title="Dashboard de Público-Alvo">
        <div className="space-y-6">
          <Suspense fallback={<DashboardSkeleton />}>
            <DashboardPublicoAlvoContent />
          </Suspense>
        </div>
      </MainLayout>
    </ErrorBoundary>
  );
}
