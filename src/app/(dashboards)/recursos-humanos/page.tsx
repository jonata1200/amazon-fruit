// src/app/(dashboards)/recursos-humanos/page.tsx
'use client';

import { lazy, Suspense } from 'react';
import { MainLayout } from '@/components/layouts/main-layout';
import { DashboardSkeleton } from '@/components/dashboards/dashboard-skeleton';
import { useAppInitialization } from '@/lib/hooks/useAppInitialization';
import { LoadingScreen } from '@/components/ui/loading-screen';
import { ErrorBoundary } from '@/components/error-boundary';

const DashboardRHContent = lazy(() =>
  import('@/components/dashboards/recursos-humanos/dashboard-rh-content').then((module) => ({
    default: module.DashboardRHContent,
  }))
);

export default function DashboardRecursosHumanosPage() {
  const { isReady } = useAppInitialization();

  if (!isReady) {
    return <LoadingScreen message="Inicializando aplicação..." />;
  }

  return (
    <ErrorBoundary title="Erro no Dashboard de Recursos Humanos" message="Ocorreu um erro ao carregar o dashboard de recursos humanos.">
      <MainLayout title="Dashboard de Recursos Humanos">
        <div className="space-y-6">
          <Suspense fallback={<DashboardSkeleton />}>
            <DashboardRHContent />
          </Suspense>
        </div>
      </MainLayout>
    </ErrorBoundary>
  );
}
